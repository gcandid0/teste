from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from math import log
import json
from . import estados as std

# Inicializa instância de gas
if not hasattr(std, 'instancia_gas'):
    std.instancia_gas = std.gas_cls()

gas = std.instancia_gas

# Garante lista_gas
if not hasattr(gas, 'lista_gas') or gas.lista_gas is None:
    gas.lista_gas = []

from .forms import (
    ConstantesPCte8, ConstantesPCte8_2,
    PGasIdeal8, Prop1PCte8, Prop2PCte8, TvizGasIdeal8
)

# Funções Auxiliares
def to_kelvin(T): return T + 273.15 if T is not None else None
def to_celsius(T): return T - 273.15 if T is not None else None
def rd(x): return round(x, 4) if x is not None else None

###############################################################################
# VIEWS DE FORMULÁRIO
###############################################################################

def ask_known1_view8(request):
    try:
        gas.limpar_gas()
    except Exception:
        gas.lista_gas = []
    request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)

    if request.method == 'POST':
        form = ConstantesPCte8(request.POST)
        if form.is_valid():
            request.session['property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known2_8')
    else:
        form = ConstantesPCte8()
    return render(request, 'ask_known1_8.html', {'form': form})

def ask_known2_view8(request):
    prop = request.session.get('property_choice')
    excluded = [str(prop)] if prop is not None else []

    if request.method == 'POST':
        form = ConstantesPCte8_2(request.POST, excluded_properties=excluded)
        if form.is_valid():
            second_property_choice = int(form.cleaned_data['property_choice'])
            second_value_input = float(form.cleaned_data['value_input'])
            
            # Validação de Constantes
            const1 = int(request.session.get('property_choice'))
            val1 = float(request.session.get('value_input'))
            const_values = {const1: val1, second_property_choice: second_value_input}
            
            Cv0 = const_values.get(11); Cp0 = const_values.get(12)
            R = const_values.get(13); K = const_values.get(14)

            # Lógica de determinação cruzada
            if Cp0 is not None and Cv0 is not None:
                R = Cp0 - Cv0; K = Cp0 / Cv0 if Cv0 else None
            elif Cp0 is not None and R is not None:
                Cv0 = Cp0 - R; K = Cp0 / Cv0 if Cv0 else None
            elif Cv0 is not None and R is not None:
                Cp0 = Cv0 + R; K = Cp0 / Cv0 if Cv0 else None
            elif R is not None and K is not None:
                if K != 1:
                    Cv0 = R / (K - 1); Cp0 = K * Cv0

            error_messages = []
            if R is not None and R <= 0: error_messages.append("R deve ser positivo.")
            if K is not None and K <= 1: error_messages.append("K deve ser maior que 1.")
            
            if error_messages:
                context = {"Cv0": Cv0, "Cp0": Cp0, "R": R, "K": K, "error_messages": error_messages}
                return render(request, "error_constants8.html", context)

            request.session['second_property_choice'] = second_property_choice
            request.session['second_value_input'] = second_value_input
            return redirect('ask_known3_8')
    else:
        form = ConstantesPCte8_2(excluded_properties=excluded)
    return render(request, 'ask_known2_8.html', {'form': form})

def ask_known3_view8(request):
    if request.method == 'POST':
        form = PGasIdeal8(request.POST)
        if form.is_valid():
            request.session['P_value_input'] = float(form.cleaned_data['P_value_input'])
            return redirect('ask_known4_8')
    else:
        form = PGasIdeal8()
    return render(request, 'ask_known3_8.html', {'form': form})

def ask_known4_view8(request):
    if request.method == 'POST':
        form = Prop1PCte8(request.POST)
        if form.is_valid():
            request.session['third_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['third_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known5_8')
    else:
        form = Prop1PCte8()
    return render(request, 'ask_known4_8.html', {'form': form})

def ask_known5_view8(request):
    if request.method == 'POST':
        form = Prop2PCte8(request.POST)
        if form.is_valid():
            request.session['four_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['four_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known6_8')
    else:
        form = Prop2PCte8()
    return render(request, 'ask_known5_8.html', {'form': form})

def ask_known6_view8(request):
    if request.method == 'POST':
        form = TvizGasIdeal8(request.POST)
        if form.is_valid():
            request.session['Tviz_value_input'] = float(form.cleaned_data['Tviz_value_input'])
            return redirect('process_values_8')
    else:
        form = TvizGasIdeal8()
    return render(request, 'ask_known6_8.html', {'form': form})

###############################################################################
# CÁLCULOS FINAIS (PRESSÃO CONSTANTE)
###############################################################################

def process_values_view8(request):
    try:
        # Recupera Inputs da Sessão
        P_input = float(request.session.get('P_value_input')) # kPa
        Tviz_input = float(request.session.get('Tviz_value_input')) # °C
        
        c1_idx = int(request.session.get('property_choice'))
        c1_val = float(request.session.get('value_input'))
        c2_idx = int(request.session.get('second_property_choice'))
        c2_val = float(request.session.get('second_value_input'))
        
        prop1_idx = int(request.session.get('third_property_choice')) # 0=T, 2=v, 8=Q
        prop1_val = float(request.session.get('third_value_input'))
        
        prop2_idx = int(request.session.get('four_property_choice')) # 0=T, 2=v, 8=Q
        prop2_val = float(request.session.get('four_value_input'))

        # --- 1. Definição de Constantes ---
        map_const = {c1_idx: c1_val, c2_idx: c2_val}
        Cv0 = map_const.get(11); Cp0 = map_const.get(12)
        R = map_const.get(13); K = map_const.get(14)

        if Cp0 is not None and Cv0 is not None: R = Cp0 - Cv0
        elif Cp0 is not None and R is not None: Cv0 = Cp0 - R
        elif Cv0 is not None and R is not None: Cp0 = Cv0 + R
        
        # Se faltar Cp0 mas tiver R e K
        if Cp0 is None and R is not None and K is not None:
             Cv0 = R / (K - 1)
             Cp0 = K * Cv0

        if R is None or Cp0 is None:
            return redirect('error_type8')

        # --- 2. Definição do Estado 1 (Inicial) ---
        T1 = None # Kelvin
        v1 = None 
        p1 = P_input # Isobárico: p1 = p2 = P_input

        # Tenta usar estado anterior (se p for igual, é continuação isobárica)
        usar_anterior = False
        if gas.lista_gas:
            ultimo = gas.lista_gas[-1]
            if len(ultimo) >= 7:
                # [Cv, Cp, R, K, p, T_C, v]
                p_last = ultimo[4]
                t_last_c = ultimo[5]
                v_last = ultimo[6]
                
                # Se a pressão do input for a mesma do estado anterior, assume continuação
                if abs(p_last - P_input) < 0.1:
                    T1 = to_kelvin(t_last_c)
                    v1 = v_last
                    p1 = p_last
                    usar_anterior = True

        if not usar_anterior:
            if prop1_idx == 0: # T1 fornecido em °C
                T1 = to_kelvin(prop1_val)
                v1 = (R * T1) / p1
            elif prop1_idx == 2: # v1 fornecido
                v1 = prop1_val
                T1 = (p1 * v1) / R

        # --- 3. Definição do Estado 2 (Final) ---
        T2 = None # Kelvin
        v2 = None
        p2 = p1 # Isobárico
        Q12_input = None

        if prop2_idx == 0: # T2 fornecido em °C
            T2 = to_kelvin(prop2_val)
            v2 = (R * T2) / p2
        elif prop2_idx == 2: # v2 fornecido
            v2 = prop2_val
            T2 = (p2 * v2) / R
        elif prop2_idx == 8: # Calor fornecido
            Q12_input = prop2_val
            # Q = Cp * (T2 - T1) => T2 = T1 + Q/Cp
            if T1 is not None and Cp0 is not None:
                T2 = T1 + (Q12_input / Cp0)
                v2 = (R * T2) / p2

        # Validação Física
        if T1 is None or T2 is None or v1 is None or v2 is None:
             return redirect('error_type8')
        if T1 <= 0 or T2 <= 0 or v1 <= 0 or v2 <= 0:
             return redirect('error_type8')

        # --- 4. Cálculos do Processo ---
        # Isobárico: W = p * (v2 - v1)
        # Q = Cp * (T2 - T1) ou Delta H
        
        W12 = p1 * (v2 - v1)
        
        if Q12_input is not None:
            Q12 = Q12_input
        else:
            Q12 = Cp0 * (T2 - T1)

        # Entropia Gerada
        # Delta S = Cp * ln(T2/T1) - R * ln(p2/p1). Como p2=p1, termo R zera.
        # Sger = Delta S - Q/Tviz
        
        Tviz_K = to_kelvin(Tviz_input)
        try:
            delta_S = Cp0 * log(T2 / T1)
            Sger = delta_S - (Q12 / Tviz_K)
        except (ValueError, ZeroDivisionError):
            Sger = 0

        # --- 5. Salvar e Renderizar ---
        # Salva o estado FINAL na lista (em Celsius)
        T2_C = to_celsius(T2)
        novo_estado = [
            float(Cv0) if Cv0 else 0,
            float(Cp0) if Cp0 else 0,
            float(R),
            float(K) if K else 0,
            float(p2),
            float(T2_C),
            float(v2)
        ]
        gas.lista_gas.append(novo_estado)
        request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)

        context = {
            'Cv0': rd(Cv0), 'Cp0': rd(Cp0), 'R': rd(R), 'K': rd(K),
            'p': rd(p1),
            'T1': rd(to_celsius(T1)), 'T2': rd(T2_C),
            'v1': rd(v1), 'v2': rd(v2),
            'Q12': rd(Q12), 'W12': rd(W12),
            'Sger': rd(Sger), 'Tviz': rd(Tviz_input),
            'teste': gas.lista_gas
        }

        return render(request, 'results_8.html', context)

    except Exception as e:
        print(f"Erro process_values_8: {e}")
        return redirect('error_type8')

def error_type_view8(request):
    return render(request, 'error_type7.html')
