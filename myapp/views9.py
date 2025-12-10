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
    ConstantesVCte9, ConstantesVCte9_2,
    VGasIdeal9, Prop1VCte9, Prop2VCte9, TvizGasIdeal9
)

# Funções Auxiliares
def to_kelvin(T): return T + 273.15 if T is not None else None
def to_celsius(T): return T - 273.15 if T is not None else None
def rd(x): return round(x, 4) if x is not None else None

###############################################################################
# VIEWS DE FORMULÁRIO (Passos 1 a 6)
###############################################################################

def ask_known1_view9(request):
    try:
        gas.limpar_gas()
    except Exception:
        gas.lista_gas = []
    request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)
    
    if request.method == 'POST':
        form = ConstantesVCte9(request.POST)
        if form.is_valid():
            request.session['property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known2_9')
    else:
        form = ConstantesVCte9()
    return render(request, 'ask_known1_9.html', {'form': form})

def ask_known2_view9(request):
    prop = request.session.get('property_choice')
    excluded = [str(prop)] if prop is not None else []

    if request.method == 'POST':
        form = ConstantesVCte9_2(request.POST, excluded_properties=excluded)
        if form.is_valid():
            second_property_choice = int(form.cleaned_data['property_choice'])
            second_value_input = float(form.cleaned_data['value_input'])
            
            # Validação
            const1 = int(request.session.get('property_choice'))
            val1 = float(request.session.get('value_input'))
            const_values = {const1: val1, second_property_choice: second_value_input}
            
            Cv0 = const_values.get(11); Cp0 = const_values.get(12)
            R = const_values.get(13); K = const_values.get(14)
            
            # Lógica Cruzada
            if Cp0 is not None and Cv0 is not None: 
                R = Cp0 - Cv0; K = Cp0/Cv0 if Cv0 else None
            elif Cp0 is not None and R is not None: 
                Cv0 = Cp0 - R; K = Cp0/Cv0 if Cv0 else None
            elif Cv0 is not None and R is not None: 
                Cp0 = Cv0 + R; K = Cp0/Cv0 if Cv0 else None
            elif R is not None and K is not None and (K-1)!=0: 
                Cv0 = R/(K-1); Cp0 = K*Cv0

            error_messages = []
            if R is not None and R <= 0: error_messages.append("R deve ser positivo.")
            
            if error_messages:
                context = {"Cv0": Cv0, "Cp0": Cp0, "R": R, "K": K, "error_messages": error_messages}
                return render(request, "error_constants8.html", context) 

            request.session['second_property_choice'] = second_property_choice
            request.session['second_value_input'] = second_value_input
            return redirect('ask_known3_9')
    else:
        form = ConstantesVCte9_2(excluded_properties=excluded)
    return render(request, 'ask_known2_9.html', {'form': form})

def ask_known3_view9(request):
    if request.method == 'POST':
        form = VGasIdeal9(request.POST)
        if form.is_valid():
            request.session['V_value_input'] = float(form.cleaned_data['V_value_input'])
            return redirect('ask_known4_9')
    else:
        form = VGasIdeal9()
    return render(request, 'ask_known3_9.html', {'form': form})

def ask_known4_view9(request):
    if request.method == 'POST':
        form = Prop1VCte9(request.POST)
        if form.is_valid():
            request.session['third_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['third_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known5_9')
    else:
        form = Prop1VCte9()
    return render(request, 'ask_known4_9.html', {'form': form})

def ask_known5_view9(request):
    if request.method == 'POST':
        form = Prop2VCte9(request.POST)
        if form.is_valid():
            request.session['four_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['four_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known6_9')
    else:
        form = Prop2VCte9()
    return render(request, 'ask_known5_9.html', {'form': form})

def ask_known6_view9(request):
    if request.method == 'POST':
        form = TvizGasIdeal9(request.POST)
        if form.is_valid():
            request.session['Tviz_value_input'] = float(form.cleaned_data['Tviz_value_input'])
            return redirect('process_values_9')
    else:
        form = TvizGasIdeal9()
    return render(request, 'ask_known6_9.html', {'form': form})

###############################################################################
# CÁLCULOS FINAIS (VOLUME CONSTANTE)
###############################################################################

def process_values_view9(request):
    try:
        # Recupera dados
        V_input = float(request.session.get('V_value_input'))
        Tviz_input = float(request.session.get('Tviz_value_input'))
        
        c1_idx = int(request.session.get('property_choice'))
        c1_val = float(request.session.get('value_input'))
        c2_idx = int(request.session.get('second_property_choice'))
        c2_val = float(request.session.get('second_value_input'))
        
        prop1_idx = int(request.session.get('third_property_choice')) # 0=T, 1=P, 8=Q
        prop1_val = float(request.session.get('third_value_input'))
        
        prop2_idx = int(request.session.get('four_property_choice')) # 0=T, 1=P, 8=Q
        prop2_val = float(request.session.get('four_value_input'))

        # --- 1. Constantes ---
        map_const = {c1_idx: c1_val, c2_idx: c2_val}
        Cv0 = map_const.get(11); Cp0 = map_const.get(12)
        R = map_const.get(13); K = map_const.get(14)

        if Cp0 is not None and Cv0 is not None: R = Cp0 - Cv0
        elif Cp0 is not None and R is not None: Cv0 = Cp0 - R
        elif Cv0 is not None and R is not None: Cp0 = Cv0 + R
        
        if Cv0 is None and R is not None and K is not None:
             Cv0 = R / (K - 1)
             Cp0 = K * Cv0

        if R is None or Cv0 is None:
            return redirect('error_type9')
            
        # CORREÇÃO: Garante que K seja calculado se estiver faltando
        if K is None and Cp0 is not None and Cv0 is not None and Cv0 != 0:
            K = Cp0 / Cv0

        # --- 2. Estado 1 ---
        T1 = None # Kelvin
        p1 = None
        v1 = V_input # Isocórico: v1 = v2 = V_input

        # Tenta usar estado anterior (se v for igual, é continuação isocórica)
        usar_anterior = False
        if gas.lista_gas:
            ultimo = gas.lista_gas[-1]
            if len(ultimo) >= 7:
                # [Cv, Cp, R, K, p, T_C, v]
                p_last = ultimo[4]
                t_last_c = ultimo[5]
                v_last = ultimo[6]
                
                if abs(v_last - V_input) < 0.001:
                    T1 = to_kelvin(t_last_c)
                    p1 = p_last
                    v1 = v_last
                    usar_anterior = True

        if not usar_anterior:
            if prop1_idx == 0: # T1 fornecido
                T1 = to_kelvin(prop1_val)
                p1 = (R * T1) / v1
            elif prop1_idx == 1: # p1 fornecido
                p1 = prop1_val
                T1 = (p1 * v1) / R

        # --- 3. Estado 2 ---
        T2 = None # Kelvin
        p2 = None
        v2 = v1
        Q12_input = None

        if prop2_idx == 0: # T2 fornecido
            T2 = to_kelvin(prop2_val)
            p2 = (R * T2) / v2
        elif prop2_idx == 1: # p2 fornecido
            p2 = prop2_val
            T2 = (p2 * v2) / R
        elif prop2_idx == 8: # Calor fornecido
            Q12_input = prop2_val
            # Q = Cv * (T2 - T1) => T2 = T1 + Q/Cv
            if T1 is not None and Cv0 is not None:
                T2 = T1 + (Q12_input / Cv0)
                p2 = (R * T2) / v2

        # Validação Física (Comentada para permitir visualizar resultados negativos/estranhos)
        if T1 is None or T2 is None or p1 is None or p2 is None:
             return redirect('error_type9')
        # if T1 <= 0 or T2 <= 0 or p1 <= 0 or p2 <= 0:
        #      return redirect('error_type9')

        # --- 4. Cálculos do Processo ---
        W12 = 0 # Isocórico
        
        if Q12_input is not None:
            Q12 = Q12_input
        else:
            Q12 = Cv0 * (T2 - T1)

        # Entropia Gerada
        # Delta S = Cv * ln(T2/T1) + R * ln(v2/v1). Como v2=v1, termo R zera.
        # Sger = Delta S - Q/Tviz
        
        Tviz_K = to_kelvin(Tviz_input)
        try:
            if T1 > 0 and T2 > 0:
                delta_S = Cv0 * log(T2 / T1)
                Sger = delta_S - (Q12 / Tviz_K)
            else:
                Sger = None
        except (ValueError, ZeroDivisionError):
            Sger = 0

        # --- 5. Salvar e Renderizar ---
        T2_C = to_celsius(T2)
        
        # Salva o novo estado mesmo se for "fisicamente impossível"
        novo_estado = [
            float(Cv0) if Cv0 else 0,
            float(Cp0) if Cp0 else 0,
            float(R),
            float(K) if K else 0,
            float(p2) if p2 else 0,
            float(T2_C) if T2_C is not None else 0,
            float(v2)
        ]
        gas.lista_gas.append(novo_estado)
        request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)

        context = {
            'Cv0': rd(Cv0), 'Cp0': rd(Cp0), 'R': rd(R), 'K': rd(K),
            'V': rd(v1),
            'T1': rd(to_celsius(T1)), 'T2': rd(T2_C),
            'p1': rd(p1), 'p2': rd(p2),
            'Q12': rd(Q12), 'W12': rd(W12),
            'Sger': rd(Sger), 'Tviz': rd(Tviz_input),
            'teste': gas.lista_gas
        }

        return render(request, 'results_9.html', context)

    except Exception as e:
        print(f"Erro process_values_9: {e}")
        return redirect('error_type9')

def error_type_view9(request):
    return render(request, 'error_type7.html')