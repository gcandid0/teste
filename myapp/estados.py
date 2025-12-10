# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 08:36:26 2025

@author: gabri
"""

class estados_cls:
    """ESTADOS"""
    
    classe = 'Estados'
    
    def __init__(self, lista_estados=None):
        self.lista_estados = []

    def limpar_estados(self):
        self.lista_estados.clear()
        
class gas_cls:
    """
    Classe de armazenamento dos estados de gás.
    Cada estado salvo segue a estrutura:
    [Cv0, Cp0, R, K, p, T, v]
    Todas as grandezas salvo em forma numérica.
    """

    classe = 'Gas'

    def __init__(self):
        # Lista onde cada item é um estado completo
        self.lista_gas = []

    # ---------------------------------------------------------
    # Limpa completamente a memória de estados
    # ---------------------------------------------------------
    def limpar_gas(self):
        self.lista_gas.clear()

    # ---------------------------------------------------------
    # Adiciona estado na forma padrão:
    # Cv0, Cp0, R, K, p (kPa), T (K), v (m³/kg)
    # ---------------------------------------------------------
    def salvar_estado(self, Cv0, Cp0, R, K, p, T, v):
        try:
            estado = [
                float(Cv0) if Cv0 is not None else None,
                float(Cp0) if Cp0 is not None else None,
                float(R) if R is not None else None,
                float(K) if K is not None else None,
                float(p) if p is not None else None,
                float(T) if T is not None else None,
                float(v) if v is not None else None,
            ]
            self.lista_gas.append(estado)
        except Exception as e:
            print("Erro ao salvar estado:", e)

    # ---------------------------------------------------------
    # Recupera o último estado COMPLETO (ou None)
    # ---------------------------------------------------------
    def ultimo_estado(self):
        if not self.lista_gas:
            return None

        ultimo = self.lista_gas[-1]

        # Tem 7 itens e todos definidos
        if (
            isinstance(ultimo, (list, tuple)) and
            len(ultimo) == 7 and
            all(x is not None for x in ultimo)
        ):
            return ultimo

        return None

    # ---------------------------------------------------------
    # Verifica se existe estado anterior consistente
    # ---------------------------------------------------------
    def tem_estado_valido(self):
        return self.ultimo_estado() is not None

    # ---------------------------------------------------------
    # Retorna dados separados (Cv0, Cp0, R, K, p, T, v)
    # ---------------------------------------------------------
    def pegar_estado_completo(self):
        ultimo = self.ultimo_estado()
        if ultimo is None:
            return None, None, None, None, None, None, None
        return tuple(ultimo)

    # ---------------------------------------------------------
    # Exibe lista para debug
    # ---------------------------------------------------------
    def print_lista(self):
        print("---- LISTA DE ESTADOS DE GÁS ----")
        for i, est in enumerate(self.lista_gas):
            print(f"{i}: {est}")
        print("----------------------------------")
