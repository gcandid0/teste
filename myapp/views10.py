from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from math import log, exp
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
    ConstantesTCte10, ConstantesTCte10_2,
    TGasIdeal10, Prop1TCte10, Prop2TCte10, TvizGasIdeal10
)

# Funções Auxiliares
def to_kelvin(T): 
    return T + 273.15 if T is not None else None

def to_celsius(T): 
    return T - 273.15 if T is not None else None

def rd(x): 
    if x is None: return None
    return round(x, 4)

###############################################################################
# VIEWS DE FORMULÁRIO (Passos 1 a 6)
###############################################################################

def ask_known1_view10(request):
    # Limpa a lista ao iniciar um novo ciclo completo
    try:
        gas.limpar_gas()
    except Exception:
        gas.lista_gas = []

    request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)
    
    if request.method == 'POST':
        form = ConstantesTCte10(request.POST)
        if form.is_valid():
            request.session['property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known2_10')
    else:
        form = ConstantesTCte10()
    return render(request, 'ask_known1_10.html', {'form': form})

def ask_known2_view10(request):
    prop = request.session.get('property_choice')
    excluded = [str(prop)] if prop is not None else []

    if request.method == 'POST':
        form = ConstantesTCte10_2(request.POST, excluded_properties=excluded)
        if form.is_valid():
            request.session['second_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['second_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known3_10')
    else:
        form = ConstantesTCte10_2(excluded_properties=excluded)
    return render(request, 'ask_known2_10.html', {'form': form})

def ask_known3_view10(request):
    if request.method == 'POST':
        form = TGasIdeal10(request.POST)
        if form.is_valid():
            request.session['T_value_input'] = float(form.cleaned_data['T_value_input'])
            return redirect('ask_known4_10')
    else:
        form = TGasIdeal10()
    return render(request, 'ask_known3_10.html', {'form': form})

def ask_known4_view10(request):
    if request.method == 'POST':
        form = Prop1TCte10(request.POST)
        if form.is_valid():
            request.session['third_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['third_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known5_10')
    else:
        form = Prop1TCte10()
    return render(request, 'ask_known4_10.html', {'form': form})

def ask_known5_view10(request):
    if request.method == 'POST':
        form = Prop2TCte10(request.POST)
        if form.is_valid():
            request.session['four_property_choice'] = int(form.cleaned_data['property_choice'])
            request.session['four_value_input'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known6_10')
    else:
        form = Prop2TCte10()
    return render(request, 'ask_known5_10.html', {'form': form})

def ask_known6_view10(request):
    if request.method == 'POST':
        form = TvizGasIdeal10(request.POST)
        if form.is_valid():
            request.session['Tviz_value_input'] = float(form.cleaned_data['Tviz_value_input'])
            return redirect('process_values_10')
    else:
        form = TvizGasIdeal10()
    return render(request, 'ask_known6_10.html', {'form': form})

###############################################################################
# LÓGICA DE CÁLCULO (Passo 7)
###############################################################################

def process_values_view10(request):
    processo_impossivel = False
    
    try:
        # --- 1. Recuperar Inputs ---
        T_input_C = float(request.session.get('T_value_input'))
        T_K = to_kelvin(T_input_C)
        Tviz_C = float(request.session.get('Tviz_value_input'))
        Tviz_K = to_kelvin(Tviz_C)

        # Constantes brutas
        c1_idx = int(request.session.get('property_choice'))
        c1_val = float(request.session.get('value_input'))
        c2_idx = int(request.session.get('second_property_choice'))
        c2_val = float(request.session.get('second_value_input'))

        # Propriedades de Estado
        p1_choice = int(request.session.get('third_property_choice')) # 1=P, 2=v
        p1_val = float(request.session.get('third_value_input'))
        
        p2_choice = int(request.session.get('four_property_choice')) # 1=P, 2=v, 8=Q
        p2_val = float(request.session.get('four_value_input'))

        # --- 2. Resolver Constantes (R, Cp, Cv, k) ---
        # 11=Cv, 12=Cp, 13=R, 14=k
        map_const = {c1_idx: c1_val, c2_idx: c2_val}
        Cv0 = map_const.get(11)
        Cp0 = map_const.get(12)
        R = map_const.get(13)
        K = map_const.get(14)

        # Lógica de determinação cruzada
        if R is None and Cp0 is not None and Cv0 is not None:
            R = Cp0 - Cv0
        if Cv0 is None and Cp0 is not None and R is not None:
            Cv0 = Cp0 - R
        if Cp0 is None and Cv0 is not None and R is not None:
            Cp0 = Cv0 + R
        
        # Se temos K e R (comum)
        if K is not None and R is not None and Cv0 is None:
            # k = (Cv+R)/Cv => k*Cv = Cv + R => Cv(k-1) = R => Cv = R/(k-1)
            if K != 1:
                Cv0 = R / (K - 1)
                Cp0 = K * Cv0
        
        # Recalcula K e R se faltar, para garantir preenchimento
        if R is None and Cp0 is not None and Cv0 is not None:
            R = Cp0 - Cv0
        if K is None and Cp0 is not None and Cv0 is not None and Cv0 != 0:
            K = Cp0 / Cv0

        # Validação básica de constantes
        if R is None or R <= 0:
            return redirect('error_type10') # R inválido

        # --- 3. Determinar Estado 1 (Inicial) ---
        p1 = None
        v1 = None

        # Tenta usar estado anterior SE a temperatura for compatível (continuidade)
        usar_anterior = False
        if gas.lista_gas:
            ultimo = gas.lista_gas[-1]
            # ultimo = [Cv, Cp, R, K, P_final, T_final_C, v_final]
            if len(ultimo) >= 7:
                t_last = ultimo[5]
                # Só aproveita o estado anterior se a temperatura for a mesma (Processo Isotérmico)
                if abs(t_last - T_input_C) < 0.1: 
                    p1 = ultimo[4]
                    v1 = ultimo[6]
                    usar_anterior = True
        
        # Se não puder usar anterior, usa o input do usuário
        if not usar_anterior:
            if p1_choice == 1: # Pressão fornecida
                p1 = p1_val
                v1 = (R * T_K) / p1
            elif p1_choice == 2: # Volume fornecido
                v1 = p1_val
                p1 = (R * T_K) / v1

        # --- 4. Determinar Estado 2 (Final) ---
        p2 = None
        v2 = None
        Q12_input = None

        if p2_choice == 1: # Pressão 2 conhecida
            p2 = p2_val
            v2 = (R * T_K) / p2
        elif p2_choice == 2: # Volume 2 conhecido
            v2 = p2_val
            p2 = (R * T_K) / v2
        elif p2_choice == 8: # Calor fornecido
            Q12_input = p2_val
            # Q = RT ln(v2/v1) => Q/RT = ln(v2/v1) => v2 = v1 * exp(Q/RT)
            if v1 and R and T_K:
                v2 = v1 * exp(Q12_input / (R * T_K))
                p2 = (R * T_K) / v2

        # --- 5. Cálculos do Processo (Isotérmico) ---
        # Q - W = Delta U. Gás Ideal T=cte => Delta U = 0 => Q = W
        
        if v1 is None or v2 is None or v1 <= 0 or v2 <= 0:
             return redirect('error_type10')

        # Trabalho e Calor
        # W = m R T ln(v2/v1)  (específico: W = R T ln(v2/v1))
        # Se o calor foi input, usamos ele para consistência, senão calculamos
        if Q12_input is not None:
            Q12 = Q12_input
            W12 = Q12_input
        else:
            try:
                val_log = log(v2 / v1)
                W12 = R * T_K * val_log
                Q12 = W12
            except ValueError:
                return redirect('error_type10')

        # Entropia
        # Delta S = Cp ln(T2/T1) - R ln(P2/P1)
        # Como T1=T2 => Delta S = -R ln(P2/P1)
        # Sger = Delta S - Q/Tviz
        
        try:
            delta_S = -R * log(p2 / p1)
            S_ger = delta_S - (Q12 / Tviz_K)
            
            if S_ger < -0.0001: # Tolerância pequena
                processo_impossivel = True
        except (ValueError, ZeroDivisionError):
            S_ger = 0

        # --- 6. Salvar e Renderizar ---
        
        # Salva o novo estado na lista para o próximo passo
        # Formato: [Cv, Cp, R, K, P_final, T_final_C, v_final]
        novo_estado = [
            float(Cv0) if Cv0 else 0,
            float(Cp0) if Cp0 else 0,
            float(R),
            float(K) if K else 0,
            float(p2),
            float(T_input_C),
            float(v2)
        ]
        gas.lista_gas.append(novo_estado)
        request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)

        context = {
            'Cv0': rd(Cv0), 'Cp0': rd(Cp0), 'R': rd(R), 'K': rd(K),
            'T': rd(T_input_C),
            'p1': rd(p1), 'v1': rd(v1),
            'p2': rd(p2), 'v2': rd(v2),
            'Q12': rd(Q12), 'W12': rd(W12),
            'Sger': rd(S_ger), 'Tviz': rd(Tviz_C),
            'processo_impossivel': processo_impossivel,
            'teste': gas.lista_gas # Para debug/visualização da lista
        }

        return render(request, 'results_10.html', context)

    except Exception as e:
        print(f"Erro process_values_10: {e}")
        return redirect('error_type10')

###############################################################################
# PÁGINA DE ERRO
###############################################################################
def error_type_view10(request):
    return render(request, 'error_type7.html')