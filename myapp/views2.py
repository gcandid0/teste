from django.shortcuts import render, redirect
from .forms import PropertyForm, SecondPropertyForm
from django.core.exceptions import ValidationError
from . import tabelas as tbs

def homepage_view2(request):
    return render(request, 'Inicio.html')

###############################################################################

def ask_known1_view2(request):
        if request.method == 'POST':
            form = PropertyForm(request.POST)
            if form.is_valid():
                property_choice = form.cleaned_data['property_choice']
                value_input = form.cleaned_data['value_input']
                request.session['property_choice'] = property_choice
                request.session['value_input'] = value_input
                excluded_properties = [property_choice]
                return redirect('ask_known2_2')
        else:
            form = PropertyForm()
    
        return render(request, 'ask_known1_2.html', {'form': form})
    
###############################################################################
    
def ask_known2_view2(request):
        if request.method == 'POST':
            excluded_properties = [int(request.session.get('property_choice', 0))]
            form = SecondPropertyForm(request.POST, excluded_properties=excluded_properties)
            if form.is_valid():
                property_choice = form.cleaned_data['property_choice']
                value_input = form.cleaned_data['value_input']
                request.session['second_property_choice'] = property_choice
                request.session['second_value_input'] = value_input
                return redirect('process_values_2')
        else:
            excluded_properties = [int(request.session.get('property_choice', 0))]
            form = SecondPropertyForm(excluded_properties=excluded_properties)
    
        return render(request, 'ask_known2_2.html', {'form': form})
    
###############################################################################    
    
class agua_cls:
    """AGUA"""
    '''
    Calcula e imprime o valor das propriedades de diferentes substâncias a partir do valor conhecido de duas propriedades. Valores dados pelas tabelas B.2, B.3, B.4, B.5, B.6 e B.7.
    Exemplo:
        x = agua_cls(1)
    '''
    
    classe = 'Agua'

###############################################################################

    def __init__(self, opt, a, b, c, d):
        '''Construtor'''
        self.n = opt
        self.index1 = a
        self.index2 = b
        self.known1 = c
        self.known2 = d
        self.x = self.run()
    
   ###############################################################################

    def select_table(self, opt):
        '''Seleciona as tabelas de propriedades de acordo com a substância'''
        if opt == 1:
            self.tabela = tbs.tabelas_cls().B_1_1
            self.liq_comp = tbs.tabelas_cls().B_1_4
            self.vap_sup = tbs.tabelas_cls().B_1_3
        if opt == 2:
            self.tabela = tbs.tabelas_cls().B_2_1
            self.vap_sup = tbs.tabelas_cls().B_2_2
        if opt == 3:
            self.tabela = tbs.tabelas_cls().B_3_1
            self.vap_sup = tbs.tabelas_cls().B_3_2
        if opt == 4:
            self.tabela = tbs.tabelas_cls().B_4_1
            self.vap_sup = tbs.tabelas_cls().B_4_2
        if opt == 5:
            self.tabela = tbs.tabelas_cls().B_5_1
            self.vap_sup = tbs.tabelas_cls().B_5_2
        if opt == 6:
            self.tabela = tbs.tabelas_cls().B_6_1
            self.vap_sup = tbs.tabelas_cls().B_6_2
            self.props[0][2] = 'K'
        if opt == 7:
            self.tabela = tbs.tabelas_cls().B_7_1
            self.vap_sup = tbs.tabelas_cls().B_7_2
            self.props[0][2] = 'K'
            
        #Definindo os limites das tabelas para cada propriedade
        #Tmin, Tmax
        self.boundaries[0][0] = min(self.tabela[0][2],self.vap_sup[0][3][0][2])
        self.boundaries[0][1] = self.vap_sup[-1][3][0][-1]
        #pmin, pmax
        self.boundaries[1][0] = min(self.tabela[1][2],self.vap_sup[0][2])
        self.boundaries[1][1] = max(self.tabela[1][-1],self.vap_sup[-1][2])
        if self.n == 1: self.boundaries[1][1] = self.liq_comp[-1][2]
        #vmin, vmax
        self.boundaries[2][0] = self.tabela[2][2]
        if self.n == 1: self.boundaries[2][0] = self.liq_comp[-1][3][1][2]
        self.boundaries[2][1] = max(self.tabela[3][2],self.vap_sup[0][3][1][-1])
        #umin, umax
        self.boundaries[3][0] = self.tabela[4][2]
        umax = []
        for i in range(len(self.vap_sup)):
            a = self.vap_sup[i][3][2][2:]
            umax.append(max(a))
        self.boundaries[3][1] = max(umax)
        #hmin, hmax
        self.boundaries[4][0] = self.tabela[6][2]
        hmax = []
        for i in range(len(self.vap_sup)):
            a = self.vap_sup[i][3][3][2:]
            hmax.append(max(a))
        self.boundaries[4][1] = max(hmax)
        #smin, smax
        self.boundaries[5][0] = self.tabela[8][2]
        self.boundaries[5][1] = self.vap_sup[0][3][4][-1]
        
###############################################################################

    def find_phase(self):
        '''Determina a fase da substância: líquido comprimido, vapor superaquecido ou líquido e/ou vapor saturado(s)'''
        
        if self.index1 == 0: #prop1 = T
            self.prop1_T()  
        if self.index1 == 1: #prop1 = p
            self.prop1_p()
    
###############################################################################

    def prop1_T(self):
        '''Determina a fase da substância e as propriedades de saturação quando a propriedade 1 é T'''
        
        if self.known1 > self.tabela[0][-1]:
            self.phase = 2
            print("\nA substância encontra-se como vapor superaquecido.")
            if self.index2 == 6: #x
                self.tag_error = 1
                print("\nNão existe título na fase de vapor superaquecido!")

        else:
            self.sat_props(0,self.known1)
            
            #Comparando os valores de saturação com a segunda propriedade para determinar a fase da substância
            if self.index2 == 1: #p
                if self.known2 == self.sat_list[1][2]:
                    self.phase = 3
                    print("\nA substância encontra-se na região de saturação.")
                    print("É impossível determinar as propriedades da substância nessas condições porque, na região de saturação,"
                          +"temperatura e pressão são propriedades dependentes.")
                    print("É necessário o valor de outra propriedade independente.")
                    self.tag_error = 1
                if self.known2 > self.sat_list[1][2]:
                    self.phase = 1
                    print("\nA substância encontra-se como líquido comprimido.")
                if self.known2 < self.sat_list[1][2]:
                    self.phase = 2
                    print("\nA substância encontra-se como vapor superaquecido.")
                    
            if self.index2 > 1 and self.index2 < 6: #v, u, h, s
                if self.known2 >= self.sat_list[((self.index2)*2)-2][2] and self.known2 <= self.sat_list[((self.index2)*2)-1][2]:
                    self.phase = 3
                    print("\nA substância encontra-se na região de saturação.")
                if self.known2 < self.sat_list[((self.index2)*2)-2][2]:
                    self.phase = 1
                    print("\nA substância encontra-se como líquido comprimido.")
                if self.known2 > self.sat_list[((self.index2)*2)-1][2]:
                    self.phase = 2
                    print("\nA substância encontra-se como vapor superaquecido.")
        
            if self.index2 == 6: #x
                self.phase = 3
                print("\nA substância encontra-se na região de saturação.")
                        
###############################################################################

    def prop1_p(self):
        '''Determina a fase da substância e as propriedades de saturação quando a propriedade 1 é p'''

        #Para o caso da água, utiliza-se uma tabela de saturação em função da pressão
        if self.n == 1 and self.known1 > self.tabela[0][-1]:
            if self.index2 == 0 and self.known2 < self.tabela[1][-1]:
                self.phase = 1
                print("\nA substância encontra-se como líquido comprimido.")
            else:
                self.phase = 2
                print("\nA substância encontra-se como vapor superaquecido.")
                if self.index2 == 6: #x
                    self.tag_error = 1
                    print("\nNão existe título na fase de vapor superaquecido!")
                    
        elif self.n != 1 and self.known1 > self.tabela[1][-1]:
            if self.index2 == 0 and self.known2 < self.tabela[0][-1]:
                self.phase = 1
                print("\nA substância encontra-se como líquido comprimido.")
            else:
                self.phase = 2
                print("\nA substância encontra-se como vapor superaquecido.")
                if self.index2 == 6: #x
                    self.tag_error = 1
                    print("\nNão existe título na fase de vapor superaquecido!")
        
        else:
            if self.n == 1: self.sat_props(0,self.known1) #Água
            if self.n != 1: self.sat_props(1,self.known1) #Demais substâncias

            #Comparando os valores de saturação com a segunda propriedade para determinar a fase da substância
            if self.n == 1: ref = self.sat_list[1][2]
            if self.n != 1: ref = self.sat_list[0][2]
            if self.index2 == 0: #T
                if self.known2 == ref:
                    self.phase = 3
                    print("\nA substância encontra-se na região de saturação.")
                    print("É impossível determinar as propriedades da substância nessas condições porque, na região de saturação,"
                          +"temperatura e pressão são propriedades dependentes.")
                    print("É necessário o valor de outra propriedade independente.")
                    self.tag_error = 1
                if self.known2 < ref:
                    self.phase = 1
                    print("\nA substância encontra-se como líquido comprimido.")
                if self.known2 > ref:
                    self.phase = 2
                    print("\nA substância encontra-se como vapor superaquecido.")
                    
            if self.index2 > 1 and self.index2 < 6: #v, u, h, s
                if self.known2 >= self.sat_list[((self.index2)*2)-2][2] and self.known2 <= self.sat_list[((self.index2)*2)-1][2]:
                    self.phase = 3
                    print("\nA substância encontra-se na região de saturação.")
                if self.known2 < self.sat_list[((self.index2)*2)-2][2]:
                    self.phase = 1
                    print("\nA substância encontra-se como líquido comprimido.")
                if self.known2 > self.sat_list[((self.index2)*2)-1][2]:
                    self.phase = 2
                    print("\nA substância encontra-se como vapor superaquecido.")
        
            if self.index2 == 6: #x
                self.phase = 3
                print("\nA substância encontra-se na região de saturação.")

###############################################################################

    def find_props(self):
        '''Determina as propriedade da substância de acordo com a fase'''

        while True:
            try:
                
                if self.tag_error == 0:
                        
                    #LÍQUIDO COMPRIMIDO
                    if self.phase == 1:
                        self.props.pop(-1) #remove o título da lista de propriedades
                        #Se uma das propriedades conhecidas é p
                        if self.index1 == 1 or self.index2 == 1:
                            self.looking_for_p_in_lc()
                        #Se nenhuma das propriedades conhecidas é p. Neste caso, self.index1 = 0 (T)
                        if self.index1 != 1 and self.index2 != 1:
                            if self.n == 1: self.looking_for_not_p_in_lc()
                            else:
                                # ALTERADO AQUI PARA error_type_7
                                return redirect ('error_type_7')
                                break


                    #VAPOR SUPERAQUECIDO
                    if self.phase == 2:
                        self.props.pop(-1) #remove o título da lista de propriedades
                        #Se uma das propriedades conhecidas é p
                        if self.index1 == 1 or self.index2 == 1:
                            self.looking_for_p_in_vs()
                        #Se nenhuma das propriedades conhecidas é p. Neste caso, self.index1 = 0 (T)
                        if self.index1 != 1 and self.index2 != 1:
                            self.looking_for_not_p_in_vs()
                                            
                            
                    #REGIÃO DE SATURAÇÃO
                    if self.phase == 3:
                        if self.index1 == 0: #T
                            self.props[1][3] = self.sat_list[1][2] #pressão de saturação
                            
                        if self.index1 == 1: #p
                            if self.n == 1: self.props[0][3] = self.sat_list[1][2] #temperatura de saturação
                            if self.n != 1: self.props[0][3] = self.sat_list[0][2] #temperatura de saturação
                            
                        if self.index2 > 1 and self.index2 < 6: #v, u, h, s
                            yl_index = 2*(self.index2-1)
                            yv_index = (2*(self.index2-1))+1
                            yl = self.sat_list[yl_index][2]
                            yv = self.sat_list[yv_index][2]
                            self.props[6][3] = 100*self.calc_x(self.known2,yl,yv) #título
                        if self.index2 == 6: #x
                            self.props[6][3] = self.known2
                        titulo = self.props[6][3]/100
                        for i in range(2,6): # determinando o valor médio das propriedades com o título
                            yl_index = 2*(i-1)
                            yv_index = (2*(i-1))+1
                            yl = self.sat_list[yl_index][2]
                            yv = self.sat_list[yv_index][2]
                            self.props[i][3] = self.calc_y(titulo,yl,yv) #v, u, h, s
                            
                    self.get_props()
                    break
                
                if self.tag_error == 1: break
                
            except TypeError:
                # ALTERADO AQUI PARA error_type_7
                return redirect ('error_type_7')
                break
                
###############################################################################



###############################################################################

    def get_props(self):
        '''Retorna as propriedades da substância de acordo com os valores informados'''
        result = []
        
        # Verificar se os índices são válidos
        if not (0 <= self.index1 < len(self.props) and 0 <= self.index2 < len(self.props)):
            raise IndexError("Índices fornecidos estão fora dos limites da lista de propriedades.")
        
        header = (
            f'As propriedades de {self.subs[self.n - 1]} a {self.props[self.index1][3]} {self.props[self.index1][2]} '
            f'e {self.props[self.index2][3]} {self.props[self.index2][2]} são:'
        )
        result.append(header)
        
        for i in range(len(self.props)):
            if i != self.index1 and i != self.index2:
                if i == 2:
                    # Formatar com 6 casas decimais
                    result.append(f'{self.props[i][1]} = {round(self.props[i][3], 6):.6f} {self.props[i][2]}')
                elif i == 5:
                    # Formatar com 4 casas decimais
                    result.append(f'{self.props[i][1]} = {round(self.props[i][3], 4):.4f} {self.props[i][2]}')
            else:
                # Formatar com 2 casas decimais
                result.append(f'{self.props[i][1]} = {round(self.props[i][3], 2):.2f} {self.props[i][2]}')
        
        return result

###############################################################################


    def run(self):
        '''Executa os métodos de forma ordenada para determnação das propriedades termodinâmicas da substância'''

        #self.select_table(self.n)
        #while True:
            
        #VARIÁVEIS
        
        self.subs = ['a água', 'a amônia', 'o dióxido de carbono', 'o R-410a', 'o R-134a',
                  'o nitrogênio', 'o metano']
        self.tabela = []
        self.liq_comp = []
        self.vap_sup = []
        self.sat = []
        self.sat_list = [] #propiedades de saturação
        self.lgt = []
        self.props = [['Temperatura','T','°C',0],['Pressão','p','kPa',0],['Volume específico','v','m³/kg',0],['Energia interna específica','u','kJ/kg',0],['Entalpa específica','h','kJ/kg',0],['Entropia específica','s','kJ/kg.K',0],['Título','x','%',-1]]
        self.props[self.index1][3] = self.known1
        self.props[self.index2][3] = self.known2
        self.index_aux1 = 0 #posição na tabela
        self.index_aux2 = 0 #posição na tabela
        self.phase = 0 #fase da substância: 0-indeterminado, 1-líquido comprimido, 2-vapor superaquecido, 3-saturação
        self.tag1 = -1 #tag para identificar se o valor é igual ao tabelado
        self.tag2 = -1 #tag para identificar se o valor é igual ao tabelado
        self.tag_error = 0
        self.list_props = ['temperatura', 'pressão', 'volume específico', 'eneriga interna específica', 'entalpia específica', 'entropia específica', 'título']
        self.str_prop = ''
        self.boundaries = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,100]]
        self.results = [] #lista com os resultados da consulta
        
        
        # FUNÇÕES
        self.select_table(self.n)
        if self.n == 1 and self.index1 == 1:
            self.tabela = tbs.tabelas_cls().B_1_2  
        self.find_phase()
        self.find_props()
        #asw = input("\nDeseja consultar novamente as propriedades d" + self.subs[self.n - 1] + "? (s/n)\n\n> ")
        #if asw != 's': #break
        self.results = [self.phase, self.sat_list, self.props]
        return self.results


        '''        
        self.find_index2(self.tabela[self.index1], self.known)
        self.select_props(self.tabela, self.index1, self.index2, self.known, self.tag1)
        self.find_length(self.lista)
        self.print_values(self.gas, self.lista, self.index1, self.known, self.lgt)
        '''


    
###############################################################################
        
        #TOOLS FUNCTIONS


###############################################################################

    def interpolate(self, xm, x, xp, ym, yp):
        '''Função de interpolação linear'''
        value = (((x-xm)/(xp-xm))*(yp-ym))+ym
        return(value)

###############################################################################
    
    def calc_x(self, x, xl, xv):
        '''Função para cálculo do título'''
        value = (x-xl)/(xv-xl)
        return(value)

###############################################################################

    def calc_y(self, x, yl, yv):
        '''Função para cálculo do valor médio das propriedades na mistura de fases em função do título'''
        value = yl+(x*(yv-yl))
        return(value)

###############################################################################    
    
    def find_index(self, iterator, comp1, comp2, n, anterior=0):
        '''Função que determina a posição de uma variável na tabela'''
        for i in range(len(iterator)):
            if i >= n: #0 ou 2
                if comp1 == comp2[i]:
                    self.tag1 = 1
                    anterior = i
                    break
                elif comp1 < comp2[i]:
                    anterior = i - 1
                    self.tag1 = -1
                    break
                else: continue
        return(anterior)

###############################################################################
    
    def sat_props(self,n,known):
        '''Função que determina as propriedades de saturação da substância em função de T ou p
            n é o índice da coluna da propriedade pela qual serão determinadas a propriedades de saturação
            known é o valor da propriedade de busca'''
        
        #Determinando o indíce do valor anterior (ou do próprio valor) tabelado
        tabela = self.tabela
        self.index_aux1 = self.find_index(tabela[0], known, tabela[n], 2)
                  
        #Determinando o valor das propriedades de saturação
        a = []
        
        if self.tag1 == 1:
            for i in range(len(tabela)):                 
                b = []
                b.append(tabela[i][0])
                b.append(tabela[i][1])
                b.append(tabela[i][self.index_aux1])
                a.append(b)
                
        if self.tag1 == -1:
            for i in range(len(tabela)):
                b = []
                if i != n:
                    value = self.interpolate(tabela[n][self.index_aux1], known, tabela[n][self.index_aux1+1], tabela[i][self.index_aux1], tabela[i][self.index_aux1+1])
                    b.append(tabela[i][0])
                    b.append(tabela[i][1])
                    b.append(value)
                if i == n:
                    b.append(tabela[i][0])
                    b.append(tabela[i][1])
                    b.append(known)
                a.append(b)
        self.sat_list = a

###############################################################################

    def looking_for_p_in_lc(self):
        '''Função que determina os valores das propriedades na região de líquido comprimido quando uma das propriedades informadas é p'''
        if self.n == 1:
            tabela_lc = self.liq_comp
            self.tabela = tbs.tabelas_cls().B_1_1
        if self.index1 == 1:
            p = self.known1
            self.str_prop = self.props[self.index2][0]
        if self.index2 == 1:
            p = self.known2
        
        if (self.n == 1 and p < tabela_lc[0][2]) or (self.n != 1): #valor de p menor que a faixa constante na tabela de líquido comprimido para a água
            #Utiliza-se a aproximação que as propriedades do líquido comprimido são iguais à do líquido saturado na mesma temperatura
            #self.tabela = tbs.tabelas_cls().B_1_1
            if self.index1 == 0 or self.index2 == 0: #T
                aux_index = 0
            else: #v, u, h ou s
                aux_index = (2*self.index2) - 2
            
            
            #Determinando o indíce do valor anterior (ou do próprio valor) tabelado
            tabela = self.tabela
            if self.index1 == 1: self.index_aux1 = self.find_index(tabela[aux_index], self.known2, tabela[aux_index], 2)
            else: self.index_aux1 = self.find_index(tabela[aux_index], self.known1, tabela[aux_index], 2)

            #Determinando o valor das propriedades de saturação
            a = []
            if self.tag1 == 1:
                for i in range(len(tabela)):
                    if i % 2 == 0:
                        a.append(tabela[i][self.index_aux1])
            
            if self.tag1 == -1:
                for i in range(len(tabela)):
                    if i % 2 == 0:
                        if self.index1 == 1:
                            value = self.interpolate(tabela[aux_index][self.index_aux1], self.known2, tabela[aux_index][self.index_aux1+1], tabela[i][self.index_aux1], tabela[i][self.index_aux1+1])
                        else:
                            value = self.interpolate(tabela[aux_index][self.index_aux1], self.known1, tabela[aux_index][self.index_aux1+1], tabela[i][self.index_aux1], tabela[i][self.index_aux1+1])
                        a.append(value)
                        
            for i in range(len(a)):
                if i != self.index2-1 and i != 0:
                    self.props[i+1][3] = a[i]
                elif i == 0:
                    self.props[i][3] = a[i]


        if self.n == 1 and p > tabela_lc[0][2]: #valor de p dentro da faixa constante na tabela de liquido comprimido para a água
            
            if p > tabela_lc[-1][2]:
                self.tag_error == 1
                self.str_prop = self.list_props[1]
                raise TypeError

            #Determinando o indíce do valor anterior (ou do próprio valor) tabelado
            anterior = 0
            for i in range(len(tabela_lc)):
                if p == tabela_lc[i][2]:
                    self.tag1 = 1
                    anterior = i
                    break
                elif p < tabela_lc[i][2]:
                    anterior = i - 1
                    self.tag1 = -1
                    break
                else: continue
            self.index_aux2 = anterior
        
            #Construindo uma tabela para o valor da pressão informado
            a = []
            if self.tag1 == 1:
                for i in range(len(tabela_lc[self.index_aux2][3])): #T, v, u, h e s
                    b = []
                    for j in range(len(tabela_lc[self.index_aux2][3][0])):
                        if j > 1:
                            b.append(tabela_lc[self.index_aux2][3][i][j])
                    a.append(b)                                

            if self.tag1 == -1:
                for i in range(len(tabela_lc[self.index_aux2][3])):
                    b = []
                    for j in range(len(tabela_lc[self.index_aux2][3][0])):
                        if j > 1 and j < len(tabela_lc[self.index_aux2][3][0]) - 1:
                            value = self.interpolate(tabela_lc[self.index_aux2][2], p, tabela_lc[self.index_aux2+1][2], tabela_lc[self.index_aux2][3][i][j], tabela_lc[self.index_aux2+1][3][i][j])
                            b.append(value)
                    
                    #Incluindo as propriedades de saturação
                    if self.index1 == 0: #quando a primeira propriedade é T, é preciso alterar a lista de saturação para p
                        self.tabela = tbs.tabelas_cls().B_1_2
                        self.sat_props(0,self.known2)
                    if i == 0: 
                        b.append(self.sat_list[1][2])
                    else:
                        b.append(self.sat_list[2*i][2])
                    a.append(b)


            #Usando o valor da outra propriedade para obter o resultado final:
            other = 0
            if self.index1 == 1: #identificando a outra propriedade
                if self.index2 != 0:
                    self.str_prop = self.list_props[self.index2]
                    other = self.index2 - 1
                    min_tab = min(a[other])
                    max_tab = max(a[other])
                    if self.known2 < min_tab or self.known2 > max_tab:
                        raise TypeError
                    
                #identificando o índice na tabela
                self.index_aux2 = self.find_index(a[other], self.known2, a[other], 0)

                #Determinando o valor das outras propriedades
                b = []
                if self.tag1 == 1:
                    for i in range(len(a)):
                        if i != other: #exclui a segunda propriedade
                            if i == 0:
                                self.props[0][3] = a[i][self.index_aux2]
                            else:
                                self.props[i+1][3] = a[i][self.index_aux2]
                        
                if self.tag1 == -1:
                    for i in range(len(a)):
                        if i != other: #exclui a segunda propriedade
                            if i == 0:
                                self.props[0][3] = self.interpolate(a[other][self.index_aux2], self.known2, a[other][self.index_aux2+1], a[i][self.index_aux2], a[i][self.index_aux2+1])
                            else:
                                self.props[i+1][3] = self.interpolate(a[other][self.index_aux2], self.known2, a[other][self.index_aux2+1], a[i][self.index_aux2], a[i][self.index_aux2+1])

            
            if self.index2 == 1: #a outra propriedade é T
                self.str_prop = self.list_props[0]
                min_tab = min(a[other])
                max_tab = max(a[other])
                if self.known1 < min_tab or self.known1 > max_tab:
                    raise TypeError

                #identificando o índice na tabela
                self.index_aux2 = self.find_index(a[other], self.known1, a[other], 0)

                #Determinando o valor das outras propriedades
                b = []
                if self.tag1 == 1:
                    for i in range(len(a)):
                        if i > other: #exclui a temperatura
                            self.props[i+1][3] = a[i][self.index_aux2]
                                
                if self.tag1 == -1:
                    for i in range(len(a)):
                        if i > other: #exclui a temperatura
                            self.props[i+1][3] = self.interpolate(a[other][self.index_aux2], self.known1, a[other][self.index_aux2+1], a[i][self.index_aux2], a[i][self.index_aux2+1])

###############################################################################

    def looking_for_not_p_in_lc(self):
        '''Função que determina os valores das propriedades na região de líquido comprimido quando nenhuma das propriedades informadas é p'''
        tabela_lc = self.liq_comp
        b_anterior = []
        b_proximo = []
        for i in range(len(tabela_lc)): #identificando o índice por T na tabela, variando a cada pressão
            self.index_aux1 = self.find_index(tabela_lc[i][3][0], self.known1, tabela_lc[i][3][0], 2)
            
            b = []
            c = []
            if self.tag1 == 1:
                b.append(tabela_lc[i][2])
                for k in range(len(tabela_lc[i][3])):
                    b.append(tabela_lc[i][3][k][self.index_aux1])
                b_anterior = b
                
            if self.tag1 == -1:
                b.append(tabela_lc[i][2])
                b.append(self.known1)
                for k in range(len(tabela_lc[i][3])):
                    if k > 0:
                        value = self.interpolate(tabela_lc[i][3][0][self.index_aux1], self.known1, tabela_lc[i][3][0][self.index_aux1+1], tabela_lc[i][3][k][self.index_aux1], tabela_lc[i][3][k][self.index_aux1+1])
                        b.append(value)
                b_anterior = b
                
            if self.known2 == b_anterior[self.index2-1]: #casos onde os valores das 2 propriedades estão na tabela
                for k in range(len(b_anterior)):
                    if k != self.index2-1:
                        self.props[k+1][3] = b_anterior[k]
                break
            
            if i == len(tabela_lc) - 1: #caso o valor da segunda propriedade não esteja contido na tabela (erro)
                self.str_prop = self.list_props[self.index2]
                raise TypeError
                
            c.append(tabela_lc[i+1][2])
            for k in range(len(tabela_lc[i+1][3])):
                value = self.interpolate(tabela_lc[i+1][3][0][self.index_aux1], self.known1, tabela_lc[i+1][3][0][self.index_aux1+1], tabela_lc[i+1][3][k][self.index_aux1], tabela_lc[i+1][3][k][self.index_aux1+1])
                c.append(value)
            b_proximo = c
            
            #Alternado a posição de T e p nas listas
            p_aux = [b_anterior[0], b_proximo[0]]
            b_anterior[0] = b_anterior[1]
            b_proximo[0] = b_proximo[1]
            b_anterior[1] = p_aux[0]
            b_proximo[1] = p_aux[1]
            
            if (self.index2 == 4 and self.known2 < b_proximo[self.index2] and i < len(tabela_lc)-1) or (self.index2 != 4 and self.known2 > b_proximo[self.index2] and i < len(tabela_lc)-1):
            #h é a única propriedade dentre v, u, h e s que aumenta com a pressão
                for k in range(len(b_anterior)):
                    if k != 0 and k != self.index2:
                        value = self.interpolate(b_anterior[self.index2], self.known2, b_proximo[self.index2], b_anterior[k], b_proximo[k])
                        self.props[k][3] = value
                break

###############################################################################

    def looking_for_p_in_vs(self):
        '''Função que determina os valores das propriedades na região de vapor superaquecido quando uma das propriedades informadas é p'''
        tabela_vs = self.vap_sup
        if self.index1 == 1:
            p = self.known1
            self.str_prop = self.props[self.index2][0]
        if self.index2 == 1:
            p = self.known2
            
        if p > tabela_vs[-1][2] or p < tabela_vs[0][2]: #valor de p dentro da faixa constante na tabela
            self.tag_error == 1
            self.str_prop = self.list_props[1]
            raise TypeError
            
        #Determinando o indíce do valor anterior (ou do próprio valor) tabelado
        anterior = 0
        for i in range(len(tabela_vs)):
            if p == tabela_vs[i][2]:
                self.tag1 = 1
                anterior = i
                break
            elif p < tabela_vs[i][2]:
                anterior = i - 1
                self.tag1 = -1
                break
            else: continue
        self.index_aux2 = anterior
    
        #Construindo uma tabela para o valor da pressão informado
        a = []
        if self.tag1 == 1:
            for i in range(len(tabela_vs[self.index_aux2][3])): #T, v, u, h e s
                b = []
                for j in range(len(tabela_vs[self.index_aux2][3][0])):
                    if j > 1:
                        b.append(tabela_vs[self.index_aux2][3][i][j])
                a.append(b)
                

        if self.tag1 == -1: #Removendo o elemento 1 da primeira tabela para igualar a quantidade de elementos
            marcador = 0
            if tabela_vs[self.index_aux2][3][0][3] != tabela_vs[self.index_aux2+1][3][0][3]: marcador = 1
            #print(self.vap_sup)
            for i in range(len(tabela_vs[self.index_aux2][3])):
                if marcador == 1: del tabela_vs[self.index_aux2][3][i][3]

                b = []
                #Incluindo as propriedades de saturação
                if self.index1 == 0: #quando a primeira propriedade é T, é preciso alterar a lista de saturação para p
                    if self.n == 1:
                        self.tabela = tbs.tabelas_cls().B_1_2
                        self.sat_props(0,self.known2)
                    else: self.sat_props(1,self.known2)
                if i == 0: 
                    if self.n == 1: b.append(self.sat_list[1][2])
                    else: b.append(self.sat_list[0][2])
                else:
                    b.append(self.sat_list[(2*i)+1][2])
                
                for j in range(len(tabela_vs[self.index_aux2][3][0])):
                    if j > 2 and j < len(tabela_vs[self.index_aux2][3][0]):
                        value = self.interpolate(tabela_vs[self.index_aux2][2], p, tabela_vs[self.index_aux2+1][2], tabela_vs[self.index_aux2][3][i][j], tabela_vs[self.index_aux2+1][3][i][j])
                        b.append(value)
                a.append(b)
                
        #Usando o valor da outra propriedade para obter o resultado final:
        other = 0
        if self.index1 == 1: #identificando a outra propriedade
            self.str_prop = self.list_props[self.index2]
            if self.index2 != 0:
                other = self.index2 - 1
                min_tab = min(a[other])
                max_tab = max(a[other])
                if self.known2 < min_tab or self.known2 > max_tab:
                    raise TypeError
                
            #identificando o índice na tabela
            self.index_aux1 = self.find_index(a[other], self.known2, a[other], 0)

            #Determinando o valor das outras propriedades
            b = []
            if self.tag1 == 1:
                for i in range(len(a)):
                    if i != other: #exclui a segunda propriedade
                        if i == 0:
                            self.props[0][3] = a[i][self.index_aux1]
                        else:
                            self.props[i+1][3] = a[i][self.index_aux1]
                    
            if self.tag1 == -1:
                for i in range(len(a)):
                    if i != other: #exclui a segunda propriedade
                        if i == 0:
                            self.props[0][3] = self.interpolate(a[other][self.index_aux1], self.known2, a[other][self.index_aux1+1], a[i][self.index_aux1], a[i][self.index_aux1+1])
                        else:
                            self.props[i+1][3] = self.interpolate(a[other][self.index_aux1], self.known2, a[other][self.index_aux1+1], a[i][self.index_aux1], a[i][self.index_aux1+1])

        
        if self.index2 == 1: #a outra propriedade é T
            self.str_prop = self.list_props[0]
            min_tab = min(a[other])
            max_tab = max(a[other])
            if self.known1 < min_tab or self.known1 > max_tab:
                raise TypeError

            #identificando o índice na tabela
            self.index_aux2 = self.find_index(a[other], self.known1, a[other], 0)

            #Determinando o valor das outras propriedades
            b = []
            if self.tag1 == 1:
                for i in range(len(a)):
                    if i > other: #exclui a temperatura
                        self.props[i+1][3] = a[i][self.index_aux2]
                            
            if self.tag1 == -1:
                for i in range(len(a)):
                    if i > other: #exclui a temperatura
                        self.props[i+1][3] = self.interpolate(a[other][self.index_aux2], self.known1, a[other][self.index_aux2+1], a[i][self.index_aux2], a[i][self.index_aux2+1])

###############################################################################

    def looking_for_not_p_in_vs(self):
        '''Função que determina os valores das propriedades na região de vapor superaquecido quando nenhuma das propriedades informadas é p'''
        tabela_vs = self.vap_sup
        b_anterior = []
        b_proximo = []
        for i in range(len(tabela_vs)): #identificando o índice por T na tabela, variando a cada pressão
            self.index_aux1 = self.find_index(tabela_vs[i][3][0], self.known1, tabela_vs[i][3][0], 2)
            
            b = []
            c = []
            if self.tag1 == 1:
                b.append(tabela_vs[i][2])
                for k in range(len(tabela_vs[i][3])):
                    b.append(tabela_vs[i][3][k][self.index_aux1])
                b_anterior = b
                
            if self.tag1 == -1:
                b.append(tabela_vs[i][2])
                b.append(self.known1)
                for k in range(len(tabela_vs[i][3])):
                    if k > 0:
                        value = self.interpolate(tabela_vs[i][3][0][self.index_aux1], self.known1, tabela_vs[i][3][0][self.index_aux1+1], tabela_vs[i][3][k][self.index_aux1], tabela_vs[i][3][k][self.index_aux1+1])
                        b.append(value)
                b_anterior = b
                
                  
            if self.known2 == b_anterior[self.index2-1]: #casos onde os valores das 2 propriedades estão na tabela
                for k in range(len(b_anterior)):
                    if k != self.index2-1:
                        self.props[k+1][3] = b_anterior[k]
                break
            
            if i == len(tabela_vs) - 1: #caso o valor da segunda propriedade não esteja contido na tabela (erro)
                self.str_prop = self.list_props[self.index2]
                raise TypeError

            #Removendo o elemento 1 da primeira tabela para igualar a quantidade de elementos
            marcador = 0
            if tabela_vs[i][3][0][3] != tabela_vs[i+1][3][0][3]: marcador = 1
            for j in range(len(tabela_vs[i][3])):
                if marcador == 1:
                    del tabela_vs[i][3][j][1]
                    self.index_aux1 = self.index_aux1 - 1
                    break
                
            c.append(tabela_vs[i+1][2])
            for k in range(len(tabela_vs[i+1][3])):
                try:
                    value = self.interpolate(
                        tabela_vs[i+1][3][0][self.index_aux1],
                        self.known1,
                        tabela_vs[i+1][3][0][self.index_aux1+1],
                        tabela_vs[i+1][3][k][self.index_aux1],
                        tabela_vs[i+1][3][k][self.index_aux1+1]
                    )
                except IndexError:
                    # ALTERADO AQUI PARA error_type_7
                    return redirect('error_type_7')
                c.append(value)
            b_proximo = c
            
            if self.known2 > b_proximo[self.index2] and i < len(tabela_vs)-1:
            #h é a única propriedade dentre v, u, h e s que aumenta com a pressão                                    
                for k in range(len(b_anterior)):
                    if k != 1 and k != self.index2:
                        value = self.interpolate(b_anterior[self.index2], self.known2, b_proximo[self.index2], b_anterior[k], b_proximo[k])
                        self.props[k][3] = value
                self.props[1][3] = self.props[0][3]
                self.props[0][3] = self.known1
                break
            
            

###############################################################################

def process_values_view2(request):
    if 'property_choice' not in request.session or 'second_property_choice' not in request.session:
        return redirect('ask_known1_2')
    
    try:
        property_choice = int(request.session.get('property_choice'))
        second_property_choice = int(request.session.get('second_property_choice'))
        value_input = float(request.session.get('value_input'))
        second_value_input = float(request.session.get('second_value_input'))
        
        # Instanciando a classe agua_cls com os parâmetros fornecidos
        h = agua_cls(1, property_choice, second_property_choice, value_input, second_value_input)   
        

        fase = h.results[0]
        
        # Tentativa de arredondamento com validação (Igual ao views.py)
        try:
            pressao = round(h.results[2][1][3], 2)
            temperatura = round(h.results[2][0][3], 2)
            volume_esp = round(h.results[2][2][3], 8)
            energia_int = round(h.results[2][3][3], 2)
            entalpia_esp = round(h.results[2][4][3], 2)
            entropia_esp = round(h.results[2][5][3], 4)
        except (IndexError, TypeError):
             return redirect('error_type_7')

        # === VALIDAÇÃO DE INTEGRIDADE (CONTRA RESULTADOS ZERADOS) ===
        if (energia_int == 0 and entalpia_esp == 0 and entropia_esp == 0) or volume_esp == 0:
            return redirect('error_type_7')
        
        if pressao == 0 and entropia_esp == 0:
             return redirect('error_type_7')
        # ============================================================
        
        if fase == 3:
            tit = round(h.results[2][6][3], 2) 
            try:
                volume_v = h.results[1][3][2]
                volume_l = h.results[1][2][2]
                VolumeL = round((1 - (tit / 100)) * volume_l,8)
                VolumeV = (tit/100) * volume_v
            except (IndexError, TypeError):
                return redirect('error_type_7')
        else:
            tit = None
            VolumeL = None
            VolumeV = None

        try:
            volume_v = h.results[1][3][2]  # Tentativa de acessar o índice
        except IndexError:
            volume_v = None  # Define um valor padrão caso haja erro
        
        try:
            volume_l = h.results[1][3][1]  # Supondo que precise do mesmo tratamento
        except IndexError:
            volume_l = None
            
        # Se qualquer um dos valores for None, redireciona para a página de erro
        if volume_v is None or volume_l is None:
            # ALTERADO AQUI PARA error_type_7
            return redirect('error_type_7')

        teste = h.results
        
        
        return render(request, 'results_2.html', {
            'fase': fase,      
            'temperatura': temperatura,
            'pressao': pressao,
            'volume_especifico': volume_esp,      
            'energia_interna': energia_int,
            'entalpia_especifica': entalpia_esp,
            'entropia_especifica': entropia_esp,
            'teste': teste,
            'titulo': tit,
            'VolumeV': VolumeV,
            'VolumeL': VolumeL,
            'volume_v': volume_v,
            'volume_l': volume_l,
        })

    except ValidationError as e:
        # ALTERADO AQUI PARA error_type7.html
        return render(request, 'error_type7.html', {'message': str(e)})


            
###############################################################################
                
            
class BoundariesException(Exception):
    pass


###############################################################################
                
            
class TituloException(Exception):
    pass


###############################################################################

def error_value_view2(request):
    # Renderiza a página de erro de valor
        # ALTERADO AQUI PARA error_type7.html
        return render(request, 'error_type7.html')
    
# RENOMEADA E APONTADA PARA O TEMPLATE NOVO
def error_type_view7(request):
    # Renderiza a página de erro de tipo
        return render(request, 'error_type7.html')