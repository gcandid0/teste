from django import forms

class Processos(forms.Form):
    PROCESSOS_CHOICES = [
        (100, 'Aquecimento/Resfriamento à pressão constante'),
        (101, 'Aquecimento/Resfriamento à volume constante'),
        (102, 'Compressão/Expansão adiabática e reversível'),
    ]


class PropertyForm(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            (3, 'Energia Interna (u)'),
            (4, 'Entalpia específica (h)'),
            (5, 'Entropia específica (s)'),
            (6, 'Título (x)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class PropertyForm3(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            (3, 'Energia Interna (u)'),
            (4, 'Entalpia específica (h)'),
            (5, 'Entropia específica (s)'),
            (6, 'Título (x)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class TempForm(forms.Form):
    property_choice = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=7
    )
    value_input = forms.CharField(label="Digite o valor da Temperatura da Vizinhança", required=True)


class ThirdPropertyForm3(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (2, 'Volume específico (v)'),
            (3, 'Energia Interna (u)'),
            (4, 'Entalpia específica (h)'),
            (5, 'Entropia específica (s)'),
            (6, 'Título (x)'),
            (8, 'Calor Transferido (Q)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)


class PropertyIso(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyIso(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            (3, 'Energia Interna (u)'),
            (4, 'Entalpia específica (h)'),
            (5, 'Entropia específica (s)'),
            (6, 'Título (x)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class ThirdPropertyIso(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)


class PropertyForm5(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyForm5(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            (3, 'Energia Interna (u)'),
            (4, 'Entalpia específica (h)'),
            (5, 'Entropia específica (s)'),
            (6, 'Título (x)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class TempForm2(forms.Form):
    property_choice = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=7
    )
    value_input = forms.CharField(label="Digite o valor da Temperatura da Vizinhança", required=True)


class ThirdPropertyForm5(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)
    
###############################################################################################


class PropertyGasIdeal1(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
        (2, 'Volume específico (v)')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyGasIdeal1(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class RGasIdeal1(forms.Form):
    property_choice = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=7
    )
    R_value_input = forms.CharField(label="Digite o valor do R", required=True)
    
###############################################################################################


class PropertyGasIdeal2(forms.Form):
    PROPERTY_CHOICES = [
        (0, 'Temperatura (T)'),
        (1, 'Pressão (p)'),
        (2, 'Volume específico (v)')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.CharField(label="Digite o valor", required=True)

class SecondPropertyGasIdeal2(forms.Form):
    def __init__(self, *args, **kwargs):
        # Recebe a lista de propriedades excluídas do construtor
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        # Define as opções do segundo formulário, excluindo as propriedades selecionadas
        all_properties = [
            (0, 'Temperatura (T)'),
            (1, 'Pressão (p)'),
            (2, 'Volume específico (v)'),
            # Adicione todas as opções possíveis aqui
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.CharField(label="Digite o valor", required=True)

class RGasIdeal2(forms.Form):
    property_choice = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=7
    )
    R_value_input = forms.CharField(label="Digite o valor do R", required=True)

###############################################################################################

# --- Primeira constante ---
class ConstantesPCte8(forms.Form):
    PROPERTY_CHOICES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda constante (exclui a primeira) ---
class ConstantesPCte8_2(forms.Form):
    def __init__(self, *args, **kwargs):
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        all_properties = [
            ('11', 'Cv0'),
            ('12', 'Cp0'),
            ('13', 'R'),
            ('14', 'K')
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 1 ---
class Prop1PCte8(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('2', 'Volume específico (v)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 2 ---
class Prop2PCte8(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('2', 'Volume específico (v)'),
        ('8', 'Calor Transferido (Q)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Pressão ---
class PGasIdeal8(forms.Form):
    P_value_input = forms.FloatField(label="Digite o valor da Pressão", required=True)


# --- Temperatura da vizinhança ---
class TvizGasIdeal8(forms.Form):
    Tviz_value_input = forms.FloatField(label="Digite o valor da Temperatura da Vizinhança", required=True)


###############################################################################################.

# --- Primeira constante ---
class ConstantesVCte9(forms.Form):
    PROPERTY_CHOICES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda constante (exclui a primeira) ---
class ConstantesVCte9_2(forms.Form):
    def __init__(self, *args, **kwargs):
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        all_properties = [
            ('11', 'Cv0'),
            ('12', 'Cp0'),
            ('13', 'R'),
            ('14', 'K')
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 1 ---
class Prop1VCte9(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 2 ---
class Prop2VCte9(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('8', 'Calor Transferido (Q)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Pressão ---
class VGasIdeal9(forms.Form):
    V_value_input = forms.FloatField(label="Digite o valor do Volume", required=True)


# --- Temperatura da vizinhança ---
class TvizGasIdeal9(forms.Form):
    Tviz_value_input = forms.FloatField(label="Digite o valor da Temperatura da Vizinhança", required=True)

###############################################################################################.

# --- Primeira constante ---
class ConstantesTCte10(forms.Form):
    PROPERTY_CHOICES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda constante (exclui a primeira) ---
class ConstantesTCte10_2(forms.Form):
    def __init__(self, *args, **kwargs):
        excluded_properties = kwargs.pop('excluded_properties', [])
        super().__init__(*args, **kwargs)

        all_properties = [
            ('11', 'Cv0'),
            ('12', 'Cp0'),
            ('13', 'R'),
            ('14', 'K')
        ]
        filtered_properties = [(num, name) for num, name in all_properties if num not in excluded_properties]
        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 1 ---
class Prop1TCte10(forms.Form):
    PROPERTY_CHOICES = [
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 2 ---
class Prop2TCte10(forms.Form):
    PROPERTY_CHOICES = [
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),    
        ('8', 'Calor Transferido (Q)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Pressão ---
class TGasIdeal10(forms.Form):
    T_value_input = forms.FloatField(label="Digite o valor do Temperatura", required=True)


# --- Temperatura da vizinhança ---
class TvizGasIdeal10(forms.Form):
    Tviz_value_input = forms.FloatField(label="Digite o valor da Temperatura da Vizinhança", required=True)
    
###############################################################################################

# --- Primeira constante ---
class ConstantesPoli11(forms.Form):
    PROPERTY_CHOICES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda constante (exclui a primeira) ---
class ConstantesPoli11_2(forms.Form):
    ALL_PROPERTIES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]

    def __init__(self, *args, excluded_properties=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Normaliza exclusões
        excluded_set = {str(x) for x in (excluded_properties or []) if x is not None}

        filtered_properties = [
            (num, name) for num, name in self.ALL_PROPERTIES if num not in excluded_set
        ]
        if not filtered_properties:
            filtered_properties = self.ALL_PROPERTIES

        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )

    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 1 ---
class Prop1Poli11(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda Propriedade do estado 1 (exclui a primeira) ---
class Prop1Poli11_2(forms.Form):
    ALL_PROPERTIES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
    ]

    def __init__(self, *args, excluded_properties=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Normaliza o tipo de exclusão (int -> str) e evita duplicatas
        excluded_set = {str(x) for x in (excluded_properties or []) if x is not None}

        filtered_properties = [
            (num, name) for num, name in self.ALL_PROPERTIES if num not in excluded_set
        ]
        # Garante que nunca fique vazio (fallback de segurança)
        if not filtered_properties:
            filtered_properties = self.ALL_PROPERTIES

        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )

    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 2 ---
class Prop2TCte11(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
        ('8', 'Calor Transferido (Q)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Expoente politrópico ---
class NGasIdeal11(forms.Form):
    N_value_input = forms.FloatField(label="Digite o valor de n", required=True)


# --- Temperatura da vizinhança ---
class TvizGasIdeal11(forms.Form):
    Tviz_value_input = forms.FloatField(
        label="Digite o valor da Temperatura da Vizinhança", required=True
    )
    
###############################################################################################

# --- Primeira constante ---
class ConstantesPoli12(forms.Form):
    PROPERTY_CHOICES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda constante (exclui a primeira) ---
class ConstantesPoli12_2(forms.Form):
    ALL_PROPERTIES = [
        ('11', 'Cv0'),
        ('12', 'Cp0'),
        ('13', 'R'),
        ('14', 'K')
    ]

    def __init__(self, *args, excluded_properties=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Normaliza exclusões
        excluded_set = {str(x) for x in (excluded_properties or []) if x is not None}

        filtered_properties = [
            (num, name) for num, name in self.ALL_PROPERTIES if num not in excluded_set
        ]
        if not filtered_properties:
            filtered_properties = self.ALL_PROPERTIES

        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )

    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 1 ---
class Prop1_12(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Segunda Propriedade do estado 1 (exclui a primeira) ---
class Prop1_2_12(forms.Form):
    ALL_PROPERTIES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
    ]

    def __init__(self, *args, excluded_properties=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Normaliza o tipo de exclusão (int -> str) e evita duplicatas
        excluded_set = {str(x) for x in (excluded_properties or []) if x is not None}

        filtered_properties = [
            (num, name) for num, name in self.ALL_PROPERTIES if num not in excluded_set
        ]
        # Garante que nunca fique vazio (fallback de segurança)
        if not filtered_properties:
            filtered_properties = self.ALL_PROPERTIES

        self.fields['property_choice'] = forms.ChoiceField(
            choices=filtered_properties,
            widget=forms.RadioSelect,
            label="Selecione a outra propriedade conhecida"
        )

    value_input = forms.FloatField(label="Digite o valor", required=True)


# --- Propriedade do estado 2 ---
class Prop2_12(forms.Form):
    PROPERTY_CHOICES = [
        ('0', 'Temperatura (T)'),
        ('1', 'Pressão (p)'),
        ('2', 'Volume específico (v)'),
        ('8', 'Calor Transferido (Q)'),
    ]
    property_choice = forms.ChoiceField(
        choices=PROPERTY_CHOICES,
        widget=forms.RadioSelect,
        label="Selecione a propriedade conhecida"
    )
    value_input = forms.FloatField(label="Digite o valor", required=True)
