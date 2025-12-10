from django.shortcuts import render, redirect
from math import log, isfinite, exp
import json
from . import estados as std # Necessário para a continuidade de estado

# Inicialização da estrutura de dados
if not hasattr(std, 'instancia_gas'):
    std.instancia_gas = std.gas_cls()

gas = std.instancia_gas

if not hasattr(gas, 'lista_gas') or gas.lista_gas is None:
    gas.lista_gas = []

from .forms import (
    ConstantesPoli12, ConstantesPoli12_2,
    Prop1_12, Prop1_2_12, Prop2_12
)

# Funções Auxiliares de Temperatura e Arredondamento
def to_kelvin(T): return T + 273.15 if T is not None else None
def to_celsius(T): return T - 273.15 if T is not None else None
def rd(x, ndigits=4):
    return round(x, ndigits) if isinstance(x, (int, float)) and isfinite(x) else None


###############################################################################
# ETAPAS DE COLETA DAS CONSTANTES E ESTADOS
# (As funções ask_known1_view12 até ask_known5_view12 foram ajustadas apenas
# na ask_known1_view12 para limpar o estado inicial).
###############################################################################
def ask_known1_view12(request):
    # Limpa a lista de processos no início de um novo ciclo
    try:
        gas.limpar_gas()
    except Exception:
        gas.lista_gas = []
    request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)
    
    if request.method == 'POST':
        form = ConstantesPoli12(request.POST)
        if form.is_valid():
            request.session['const_prop_1'] = str(form.cleaned_data['property_choice'])
            request.session['const_val_1'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known2_12')
    else:
        form = ConstantesPoli12()
    return render(request, 'ask_known1_12.html', {'form': form})


def ask_known2_view12(request):
    first = request.session.get('const_prop_1')
    excluded_properties = [str(first)] if first is not None else []

    if request.method == 'POST':
        form = ConstantesPoli12_2(request.POST, excluded_properties=excluded_properties)
        if form.is_valid():
            request.session['const_prop_2'] = str(form.cleaned_data['property_choice'])
            request.session['const_val_2'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known3_12')
    else:
        form = ConstantesPoli12_2(excluded_properties=excluded_properties)
    return render(request, 'ask_known2_12.html', {'form': form})


def ask_known3_view12(request):
    if request.method == 'POST':
        form = Prop1_12(request.POST)
        if form.is_valid():
            request.session['state1_prop_1'] = str(form.cleaned_data['property_choice'])
            request.session['state1_val_1'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known4_12')
    else:
        form = Prop1_12()
    return render(request, 'ask_known3_12.html', {'form': form})


def ask_known4_view12(request):
    first = request.session.get('state1_prop_1')
    excluded_properties = [str(first)] if first is not None else []

    if request.method == 'POST':
        form = Prop1_2_12(request.POST, excluded_properties=excluded_properties)
        if form.is_valid():
            request.session['state1_prop_2'] = str(form.cleaned_data['property_choice'])
            request.session['state1_val_2'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known5_12')
    else:
        form = Prop1_2_12(excluded_properties=excluded_properties)
    return render(request, 'ask_known4_12.html', {'form': form})


def ask_known5_view12(request):
    if request.method == 'POST':
        form = Prop2_12(request.POST)
        if form.is_valid():
            request.session['state2_prop'] = str(form.cleaned_data['property_choice'])
            request.session['state2_val'] = float(form.cleaned_data['value_input'])
            return redirect('process_values_12')
    else:
        form = Prop2_12()
    return render(request, 'ask_known5_12.html', {'form': form})


###############################################################################
# PROCESSO ISENTRÓPICO (s = constante)
###############################################################################
def process_values_view12(request):
    """
    Processo isentrópico (s = constante).
    Recupera dados da sessão, deduz constantes, aplica continuidade
    e calcula estado 2 usando relações isentrópicas (n=K).
    """
    mensagens_diag = []
    
    try:
        # 1. Recuperação de Entradas e Constantes (Usuário)
        cprop1_raw = request.session.get('const_prop_1'); cprop2_raw = request.session.get('const_prop_2')
        cval1_raw = request.session.get('const_val_1'); cval2_raw = request.session.get('const_val_2')
        s1p1_raw = request.session.get('state1_prop_1'); s1v1_raw = request.session.get('state1_val_1')
        s1p2_raw = request.session.get('state1_prop_2'); s1v2_raw = request.session.get('state1_val_2')
        s2p_raw = request.session.get('state2_prop'); s2v_raw = request.session.get('state2_val')

        if None in (cprop1_raw, cprop2_raw, cval1_raw, cval2_raw, s1p1_raw, s1v1_raw, s1p2_raw, s1v2_raw, s2p_raw, s2v_raw):
             return render(request, 'results_12.html', {'mensagem': "Dados essenciais incompletos."})

        # Conversão Inicial de Constantes
        cprop1 = int(cprop1_raw); cprop2 = int(cprop2_raw)
        cval1 = float(cval1_raw); cval2 = float(cval2_raw)
        const_values = {cprop1: cval1, cprop2: cval2}
        Cv0 = const_values.get(11); Cp0 = const_values.get(12); R = const_values.get(13); K = const_values.get(14)
        
        T1 = p1 = v1 = None; T2 = p2 = v2 = None; Q12_user = None

        # --- 2. Correlação e Deduação de Constantes ---
        try:
            if Cp0 is not None and R is not None and Cv0 is None: Cv0 = Cp0 - R
            if Cv0 is not None and R is not None and Cp0 is None: Cp0 = Cv0 + R
            if Cp0 is not None and Cv0 is not None and R is None: R = Cp0 - Cv0
            if Cp0 is not None and Cv0 is not None and K is None and abs(Cv0) > 1e-12: K = Cp0 / Cv0
        except Exception:
             mensagens_diag.append("Erro ao tentar deduzir Cv/Cp/R/K.")

        # --- 3. Continuidade de Estado (Prioridade Máxima) ---
        ultimo_valido = False
        if gas.lista_gas:
            ultimo = gas.lista_gas[-1]
            try:
                cvf, cpf, rf, kf, pf, tf_c, vf = map(float, ultimo[:7])
                
                # Se as constantes baterem, carrega o estado final como Estado 1.
                if abs(cvf - Cv0) < 1e-6 and abs(cpf - Cp0) < 1e-6:
                    T1 = to_kelvin(tf_c)
                    p1 = pf
                    v1 = vf
                    Cv0, Cp0, R, K = cvf, cpf, rf, kf 
                    ultimo_valido = True
                    mensagens_diag.append(f"Estado inicial carregado do processo anterior: T1={tf_c}°C, p1={pf}kPa, v1={vf}m³/kg.")
            except Exception:
                pass

        # --- 4. Carregar Estado 1 (Apenas se não carregado por continuidade) ---
        if not ultimo_valido:
            s1p1 = int(s1p1_raw); s1v1 = float(s1v1_raw)
            s1p2 = int(s1p2_raw); s1v2 = float(s1v2_raw)
            
            for prop, val in [(s1p1, s1v1), (s1p2, s1v2)]:
                if prop == 0: T1 = to_kelvin(float(val))
                elif prop == 1: p1 = float(val)
                elif prop == 2: v1 = float(val)

        # --- 5. Preencher Estado 1 via Gás Ideal ---
        if T1 is None and p1 is not None and v1 is not None and R is not None: T1 = p1 * v1 / R
        if v1 is None and T1 is not None and p1 is not None and R is not None and abs(p1) > 1e-12: v1 = R * T1 / p1
        if p1 is None and T1 is not None and v1 is not None and R is not None and abs(v1) > 1e-12: p1 = R * T1 / v1
        
        if None in (T1, p1, v1):
            return render(request, 'results_12.html', {'mensagem': "Estado 1 (T1, p1, v1) incompleto após cálculos iniciais."})

        # --- 6. Carregar Estado 2 e Relações Isentrópicas (n=K) ---
        s2p = int(s2p_raw); s2v = float(s2v_raw)
        
        if s2p == 0: T2 = to_kelvin(s2v)
        elif s2p == 1: p2 = s2v
        elif s2p == 2: v2 = s2v
        elif s2p == 8: Q12_user = s2v; mensagens_diag.append("Q fornecido (ignorando, processo isentrópico assume Q=0).")
        
        # O cálculo isentrópico só é possível se K for conhecido
        if K is not None and isfinite(K) and K > 1e-12:
            try:
                # Se p2 fornecido -> calcula T2 e v2
                if p2 is not None and (T2 is None or v2 is None):
                    T2 = T1 * (p2 / p1) ** ((K - 1.0) / K)
                    v2 = v1 * (p1 / p2) ** (1.0 / K)
                    mensagens_diag.append("T2/v2 obtidos via p2 isentrópico.")
                
                # Se v2 fornecido -> calcula T2 e p2
                elif v2 is not None and (T2 is None or p2 is None):
                    T2 = T1 * (v1 / v2) ** (K - 1.0)
                    p2 = p1 * (v1 / v2) ** K
                    mensagens_diag.append("T2/p2 obtidos via v2 isentrópico.")
                
                # Se T2 fornecido -> calcula v2 e p2
                elif T2 is not None and (p2 is None or v2 is None):
                    v2 = v1 * (T1 / T2) ** (1.0 / (K - 1.0))
                    p2 = p1 * (v1 / v2) ** K
                    mensagens_diag.append("v2/p2 obtidos via T2 isentrópico.")
                
                # Re-verificação Gás Ideal para finalização
                if T2 is None and p2 is not None and v2 is not None: T2 = p2 * v2 / R
                if p2 is None and T2 is not None and v2 is not None: p2 = R * T2 / v2
                if v2 is None and T2 is not None and p2 is not None: v2 = R * T2 / p2
                
            except Exception:
                mensagens_diag.append("Erro ao aplicar relações isentrópicas.")

        # --- 7. Assumir Processo Nulo se Estado 2 Incompleto ---
        if None in (T2, p2, v2):
             T2, p2, v2 = T1, p1, v1
             mensagens_diag.append("Estado 2 não pôde ser determinado, assumindo processo nulo.")
        
        if T2 <= 0 or p2 <= 0 or v2 <= 0:
             return render(request, 'results_12.html', {'mensagem': "Estado 2 resulta em temperatura/pressão/volume negativo ou zero."})

        # --- 8. Cálculos de Processo (Q=0, Sger=0, W) ---
        Q12 = 0.0
        Sger = 0.0

        W12 = None
        try:
            if R is not None and T1 is not None and T2 is not None and isfinite(K) and abs(K - 1.0) > 1e-12:
                # W = R(T2 - T1) / (1 - K)
                W12 = R * (T2 - T1) / (1.0 - K)
                mensagens_diag.append("Trabalho W12 calculado.")
            
        except Exception:
            mensagens_diag.append("Erro ao calcular W12.")

        # --- 9. Salvamento e Contexto Final ---
        T2_c = to_celsius(T2)
        try:
            if all([Cv0, Cp0, R, K, p2, T2_c, v2]):
                novo_estado = [float(Cv0), float(Cp0), float(R), float(K), float(p2), float(T2_c), float(v2)]
                gas.lista_gas.append(novo_estado)
                request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)
            else:
                 mensagens_diag.append("Não foi possível salvar novo estado: dados essenciais ausentes para persistência.")
        except Exception as e:
            mensagens_diag.append(f"Não foi possível salvar novo estado (erro): {e}")

        # Montagem do Contexto Final
        context = {
            'Cv0': rd(Cv0), 'Cp0': rd(Cp0), 'R': rd(R), 'K': rd(K),
            'T1': rd(to_celsius(T1)), 'T2': rd(to_celsius(T2)),
            'p1': rd(p1), 'p2': rd(p2), 'v1': rd(v1), 'v2': rd(v2),
            'Q12': rd(Q12), 'W12': rd(W12), 'Sger': rd(Sger),
            'mensagem': "Cálculo realizado com sucesso.",
            'mensagens': mensagens_diag,
            'teste': gas.lista_gas
        }
        
        return render(request, 'results_12.html', context)

    except Exception as e:
        print("Erro no cálculo (process_values_view12):", e)
        return redirect('error_type12')


def error_type_view12(request):
    return render(request, 'error_type7.html')