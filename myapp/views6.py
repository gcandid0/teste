from django.shortcuts import render, redirect
from .forms import PropertyGasIdeal1, SecondPropertyGasIdeal1, RGasIdeal1
from django.core.exceptions import ValidationError

def homepage_view(request):
    return render(request, 'Inicio.html')

def gasideal_view(request):
    return render(request, 'gasideal.html')

def processosgasideal_view(request):
    return render(request, 'processos2.html')


###############################################################################

def ask_known3_view6(request):
    if request.method == 'POST':
        form = RGasIdeal1(request.POST)
        if form.is_valid(): 
            # Usa get() para evitar KeyError
            R_value_input = form.cleaned_data.get('R_value_input')
            if R_value_input is not None:
                # Armazena na sessão
                request.session['R_value_input'] = R_value_input
                return redirect('ask_known1_6')
            else:
                # Campo ausente mesmo com formulário válido (raro, mas seguro tratar)
                form.add_error(None, "Erro ao processar o valor de R. Por favor, preencha corretamente.")
    else:
        form = RGasIdeal1()

    return render(request, 'ask_known3_6.html', {'form': form})

###############################################################################

def ask_known1_view6(request):
        if request.method == 'POST':
            form = PropertyGasIdeal1(request.POST)
            if form.is_valid():
                property_choice = form.cleaned_data['property_choice']
                value_input = form.cleaned_data['value_input']
                request.session['property_choice'] = property_choice
                request.session['value_input'] = value_input
                excluded_properties = [property_choice]
                return redirect('ask_known2_6')
        else:
            form = PropertyGasIdeal1()

        return render(request, 'ask_known1_6.html', {'form': form})

###############################################################################

def ask_known2_view6(request):
        if request.method == 'POST':
            excluded_properties = [int(request.session.get('property_choice', 0))]
            form = SecondPropertyGasIdeal1(request.POST, excluded_properties=excluded_properties)
            if form.is_valid():
                property_choice = form.cleaned_data['property_choice']
                value_input = form.cleaned_data['value_input']
                request.session['second_property_choice'] = property_choice
                request.session['second_value_input'] = value_input
                return redirect('process_values_6')
        else:
            excluded_properties = [int(request.session.get('property_choice', 0))]
            form = SecondPropertyGasIdeal1(excluded_properties=excluded_properties)

        return render(request, 'ask_known2_6.html', {'form': form})



###############################################################################

def process_values_view6(request):
    if 'property_choice' not in request.session or 'second_property_choice' not in request.session:
        return redirect('ask_known1_6')

    try:
        property_choice = int(request.session.get('property_choice'))
        second_property_choice = int(request.session.get('second_property_choice'))
        value_input = float(request.session.get('value_input'))
        second_value_input = float(request.session.get('second_value_input'))
        R_value_input = float(request.session.get('R_value_input'))


        if property_choice == 0 and second_property_choice == 1:
            volume = round((R_value_input * value_input) / second_value_input, 6)
            temperatura = value_input
            pressao = second_value_input

        if property_choice == 0 and second_property_choice == 2:
            pressao= round((value_input * R_value_input) / second_value_input, 6)
            temperatura = value_input
            volume = second_value_input

        if property_choice == 1 and second_property_choice == 0:
            volume = round((R_value_input * second_value_input) / value_input, 6)
            pressao = value_input
            temperatura = second_value_input

        if property_choice == 1 and second_property_choice == 2:
            temperatura = round((second_value_input * value_input) / R_value_input, 6)
            pressao = value_input
            volume = second_value_input

        if property_choice == 2 and second_property_choice == 0:
            pressao = round((second_value_input * R_value_input) / value_input, 6)
            volume = value_input
            temperatura = second_value_input

        if property_choice == 2 and second_property_choice == 1:
            temperatura = round((second_value_input * value_input) / R_value_input, 6)
            volume = value_input
            pressao = second_value_input


        return render(request, 'results_6.html', {
            'temperatura': temperatura,
            'pressao': pressao,
            'volume': volume,
            'R': R_value_input,
        })

    except ValidationError as e:
        return render(request, 'error_type.html', {'message': str(e)})
