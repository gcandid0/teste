from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from math import log, isfinite, exp
import json
from . import estados as std

# Inicialização da estrutura de dados
if not hasattr(std, 'instancia_gas'):
    std.instancia_gas = std.gas_cls()

gas = std.instancia_gas

if not hasattr(gas, 'lista_gas') or gas.lista_gas is None:
    gas.lista_gas = []

from .forms import (
    ConstantesPoli11, ConstantesPoli11_2,
    Prop1Poli11, Prop1Poli11_2, Prop2TCte11,
    NGasIdeal11, TvizGasIdeal11
)

# Funções Auxiliares de Temperatura e Arredondamento
def to_kelvin(T): return T + 273.15 if T is not None else None
def to_celsius(T): return T - 273.15 if T is not None else None
def rd(x, ndigits=4):
    return round(x, ndigits) if isinstance(x, (int, float)) and isfinite(x) else None


# --- Funções de Fluxo de Formulário (Passos 1 a 7) ---

###############################################################################
# Passo 1 – Escolha da primeira constante
###############################################################################
def ask_known1_view11(request):
    # Limpa a lista de processos no início de um novo ciclo
    try:
        gas.limpar_gas()
    except Exception:
        gas.lista_gas = []
    request.session['lista_gas'] = json.dumps(gas.lista_gas, default=str)
    
    if request.method == 'POST':
        form = ConstantesPoli11(request.POST)
        if form.is_valid():
            request.session['const_prop_1'] = str(form.cleaned_data['property_choice'])
            request.session['const_val_1'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known2_11')
    else:
        form = ConstantesPoli11()
    return render(request, 'ask_known1_11.html', {'form': form})


###############################################################################
# Passo 2 – Escolha da segunda constante (com verificação antecipada)
###############################################################################
def ask_known2_view11(request):
    prop = request.session.get('const_prop_1')
    excluded_properties = [str(prop)] if prop is not None else []

    if request.method == 'POST':
        form = ConstantesPoli11_2(request.POST, excluded_properties=excluded_properties)
        if form.is_valid():
            second_property_choice = int(form.cleaned_data['property_choice'])
            second_value_input = float(form.cleaned_data['value_input'])

            const1 = int(request.session.get('const_prop_1')); val1 = float(request.session.get('const_val_1'))
            const_values = {const1: val1, second_property_choice: second_value_input}
            Cv0 = const_values.get(11); Cp0 = const_values.get(12); R = const_values.get(13); K = const_values.get(14)
            if Cp0 is not None and Cv0 is not None: R = Cp0 - Cv0; K = (Cp0 / Cv0) if Cv0 != 0 else None
            
            error_messages = []
            if Cp0 is not None and Cv0 is not None and Cp0 <= Cv0: error_messages.append("Cp deve ser maior que Cv.")
            if error_messages:
                context = {"mensagem_erro": "Erro nas Constantes: " + ", ".join(error_messages)}
                return render(request, "error_constants10.html", context) 

            request.session['const_prop_2'] = str(second_property_choice)
            request.session['const_val_2'] = float(second_value_input)
            return redirect('ask_known3_11')

    else:
        form = ConstantesPoli11_2(excluded_properties=excluded_properties)
    return render(request, 'ask_known2_11.html', {'form': form})


###############################################################################
# Passo 3 – Primeira propriedade do estado 1
###############################################################################
def ask_known3_view11(request):
    if request.method == 'POST':
        form = Prop1Poli11(request.POST)
        if form.is_valid():
            request.session['state1_prop_1'] = str(form.cleaned_data['property_choice'])
            request.session['state1_val_1'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known4_11')
    else:
        form = Prop1Poli11()
    return render(request, 'ask_known3_11.html', {'form': form})


###############################################################################
# Passo 4 – Segunda propriedade do estado 1
###############################################################################
def ask_known4_view11(request):
    first = request.session.get('state1_prop_1')
    excluded_properties = [str(first)] if first is not None else []

    if request.method == 'POST':
        form = Prop1Poli11_2(request.POST, excluded_properties=excluded_properties)
        if form.is_valid():
            request.session['state1_prop_2'] = str(form.cleaned_data['property_choice'])
            request.session['state1_val_2'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known5_11')
    else:
        form = Prop1Poli11_2(excluded_properties=excluded_properties)
    return render(request, 'ask_known4_11.html', {'form': form})


###############################################################################
# Passo 5 – Propriedade do estado 2 (p₂, v₂ ou Q₁₂)
###############################################################################
def ask_known5_view11(request):
    if request.method == 'POST':
        form = Prop2TCte11(request.POST)
        if form.is_valid():
            request.session['state2_prop'] = str(form.cleaned_data['property_choice'])
            request.session['state2_val'] = float(form.cleaned_data['value_input'])
            return redirect('ask_known6_11')
    else:
        form = Prop2TCte11()
    return render(request, 'ask_known5_11.html', {'form': form})


###############################################################################
# Passo 6 – Expoente n
###############################################################################
def ask_known6_view11(request):
    if request.method == 'POST':
        form = NGasIdeal11(request.POST)
        if form.is_valid():
            request.session['n_value'] = float(form.cleaned_data['N_value_input'])
            return redirect('ask_known7_11')
    else:
        form = NGasIdeal11()
    return render(request, 'ask_known6_11.html', {'form': form})


###############################################################################
# Passo 7 – Temperatura da vizinhança
###############################################################################
def ask_known7_view11(request):
    if request.method == 'POST':
        form = TvizGasIdeal11(request.POST)
        if form.is_valid():
            request.session['tviz_value'] = float(form.cleaned_data['Tviz_value_input'])
            return redirect('process_values_11')
    else:
        form = TvizGasIdeal11()
    return render(request, 'ask_known7_11.html', {'form': form})


###############################################################################
# Passo 8 – Cálculos finais (Processo Politrópico)
###############################################################################
def process_values_view11(request):
    """
    Executa os cálculos do processo politrópico e garante a continuidade de estado.
    """
    mensagens_diag = []
    processo_impossivel = False
    
    try:
        # 1. Recuperação de Entradas (Variáveis de Sessão)
        cprop1 = request.session.get('const_prop_1'); cprop2 = request.session.get('const_prop_2')
        cval1 = request.session.get('const_val_1'); cval2 = request.session.get('const_val_2')
        s1p1 = request.session.get('state1_prop_1'); s1v1 = request.session.get('state1_val_1')
        s1p2 = request.session.get('state1_prop_2'); s1v2 = request.session.get('state1_val_2')
        s2p = request.session.get('state2_prop'); s2v = request.session.get('state2_val')
        n_raw = request.session.get('n_value'); tviz_raw = request.session.get('tviz_value')

        if None in (cprop1, cprop2, cval1, cval2, s1p1, s1v1, s1p2, s1v2, s2p, s2v, n_raw, tviz_raw):
            return render(request, 'results_11.html', {'mensagem': "Dados essenciais incompletos."})

        # Conversão Inicial de Constantes e Processo
        const1 = int(cprop1); const2 = int(cprop2); val1 = float(cval1); val2 = float(cval2)
        const_values = {const1: val1, const2: val2}
        Cv0 = const_values.get(11); Cp0 = const_values.get(12); R = const_values.get(13); K = const_values.get(14)
        n = float(n_raw); Tviz_c = float(tviz_raw); Tviz = to_kelvin(Tviz_c)
        
        T1 = p1 = v1 = None; T2 = p2 = v2 = None; Q12_user = None

        # --- 2. Correlação de Constantes (Completa) ---
        if Cp0 is not None and R is not None and Cv0 is None: Cv0 = Cp0 - R
        if Cv0 is not None and R is not None and Cp0 is None: Cp0 = Cv0 + R
        if Cp0 is not None and Cv0 is not None and R is None: R = Cp0 - Cv0
        if Cp0 is not None and Cv0 is not None and K is None and abs(Cv0) > 1e-12: K = Cp0 / Cv0
        if R is not None and K is not None and abs(K - 1.0) > 1e-12: 
            Cv0 = R / (K - 1.0); Cp0 = K * Cv0

        # --- 3. Continuidade de Estado (Prioridade Máxima) ---
        ultimo_valido = False
        if gas.lista_gas:
            ultimo = gas.lista_gas[-1]
            try:
                cvf, cpf, rf, kf, pf, tf_c, vf = map(float, ultimo[:7])
                
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
            first_choice = int(s1p1); first_value = float(s1v1)
            second_choice = int(s1p2); second_value = float(s1v2)
            
            for choice, value in [(first_choice, first_value), (second_choice, second_value)]:
                if choice == 0: T1 = to_kelvin(float(value)) 
                elif choice == 1: p1 = float(value)
                elif choice == 2: v1 = float(value)

        # --- 5. Preencher Estado 1 via Gás Ideal ---
        if T1 is None and p1 is not None and v1 is not None and R is not None: T1 = p1 * v1 / R
        if v1 is None and T1 is not None and p1 is not None and R is not None and abs(p1) > 1e-12: v1 = R * T1 / p1
        if p1 is None and T1 is not None and v1 is not None and R is not None and abs(v1) > 1e-12: p1 = R * T1 / v1
        
        if None in (T1, p1, v1):
            return render(request, 'results_11.html', {'mensagem': "Estado 1 (T1, p1, v1) incompleto após cálculos iniciais."})

        # --- 6. Carregar Estado 2 e Processamento Politrópico ---
        
        second_group_choice = int(s2p); second_group_value = float(s2v)
        if second_group_choice == 0: T2 = to_kelvin(second_group_value)
        elif second_group_choice == 1: p2 = second_group_value
        elif second_group_choice == 2: v2 = second_group_value
        elif second_group_choice == 8: Q12_user = second_group_value

        try:
            # 6.1. Tentar completar o estado via Gás Ideal
            if T2 is None and p2 is not None and v2 is not None and R is not None: T2 = p2 * v2 / R
            
            # 6.2. Relações Politrópicas (Lógica Revisada)
            
            # Caso n != 1 (Politrópico geral)
            if abs(n - 1.0) > 1e-12: 
                one_over_n = 1.0 / n
                one_over_n_minus_1 = 1.0 / (n - 1.0)
                
                if v2 is not None and p2 is None: # v2 conhecido
                    p2 = p1 * (v1 / v2) ** n
                    T2 = T1 * (v1 / v2) ** (n - 1.0)
                
                elif p2 is not None and v2 is None: # p2 conhecido
                    v2 = v1 * (p1 / p2) ** one_over_n
                    T2 = T1 * (v1 / v2) ** (n - 1.0) 
                
                elif T2 is not None and v2 is None: # T2 conhecido (CORREÇÃO DE ROBUSTEZ)
                    v2 = v1 * (T1 / T2) ** one_over_n_minus_1
                    p2 = p1 * (v1 / v2) ** n
            
            # Caso n = 1 (Isotérmico)
            elif abs(n - 1.0) < 1e-12:
                T2 = T1 
                if v2 is not None and p2 is None: p2 = p1 * (v1 / v2)
                elif p2 is not None and v2 is None: v2 = v1 * (p1 / p2)

            # 6.3. Re-verificação final com Gás Ideal (para preencher o que falta)
            if T2 is None and p2 is not None and v2 is not None: T2 = p2 * v2 / R
            
        except Exception:
            mensagens_diag.append("Erro ao completar estado 2 via politrópica.")

        # Assumir Processo Nulo se Estado 2 Incompleto
        if None in (T2, p2, v2):
             T2, p2, v2 = T1, p1, v1
             mensagens_diag.append("Estado 2 não pôde ser determinado, assumindo processo nulo.")
        
        if T2 <= 0 or p2 <= 0 or v2 <= 0:
             return render(request, 'results_11.html', {'mensagem': "Estado 2 resulta em temperatura/pressão/volume negativo ou zero."})

        # --- 7. Cálculos de Processo (W, Q, Sger) ---
        
        W12 = Q12 = None
        
        # Trabalho W12
        try:
            if abs(n - 1.0) > 1e-12: W12 = (p2 * v2 - p1 * v1) / (1.0 - n)
            elif R is not None and T1 is not None and v1 > 0 and v2 > 0: W12 = R * T1 * log(v2 / v1)
        except Exception: mensagens_diag.append("Erro ao calcular W12.")

        # Calor Q12 (Q = dU + W)
        Q12_calc = None
        try:
            if Cv0 is not None and W12 is not None: Q12_calc = Cv0 * (T2 - T1) + W12
        except Exception: mensagens_diag.append("Erro ao calcular Q12.")
        Q12_final = Q12_user if Q12_user is not None else Q12_calc

        # Entropia gerada Sger
        Sger = None
        if T1 == T2 and p1 == p2: # Processo Nulo - Sger = 0
            Sger = 0.0
        elif all([Cp0, R, T1, T2, p1, p2, Q12_final, Tviz]) and T1 > 0 and T2 > 0 and Tviz > 0:
            try:
                # dS = Cp*ln(T2/T1) - R*ln(p2/p1)
                delta_s = Cp0 * log(T2 / T1) - R * log(p2 / p1)
                Sger = delta_s - (Q12_final / Tviz)
                if Sger < -1e-6: processo_impossivel = True
            except Exception: mensagens_diag.append("Erro ao calcular Sger.")

        # --- 8. Salvamento e Contexto Final ---
        
        # Salva novo estado (p2, T2_c, v2) - Para encadeamento
        try:
            T2_c = to_celsius(T2)
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
            'Cv0': rd(Cv0), 'Cp0': rd(Cp0), 'R': rd(R), 'K': rd(K), 'n': rd(n),
            'T1': rd(to_celsius(T1)), 'T2': rd(to_celsius(T2)),
            'v1': rd(v1), 'v2': rd(v2), 'p1': rd(p1), 'p2': rd(p2),
            'Q12': rd(Q12_final), 'W12': rd(W12),
            'Tviz': rd(to_celsius(Tviz)), 'Sger': rd(Sger),
            'processo_impossivel': processo_impossivel,
            'mensagens': [f"PROCESSO IMPOSSÍVEL (Sger < 0)!" if processo_impossivel else "Cálculo realizado com sucesso."],
            'teste': gas.lista_gas
        }

        context['mensagens'].extend(mensagens_diag)
        return render(request, 'results_11.html', context)

    except Exception as e:
        print("Erro no cálculo geral:", e)
        return redirect('error_type11')

def error_type_view11(request):
    return render(request, 'error_type7.html')