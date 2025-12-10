from django.urls import path
# Importando a view correta error_type_view7 que definimos no views2.py
from .views2 import (
    homepage_view2, 
    ask_known1_view2, 
    ask_known2_view2, 
    process_values_view2, 
    error_value_view2, 
    error_type_view7
)

urlpatterns = [
    # Sugestão: Alterei o name para 'homepage2' para evitar conflito com a homepage do views.py
    path('', homepage_view2, name='homepage2'),  # Rota para a homepage da "tabela/"
    
    path('tabela1/', ask_known1_view2, name='ask_known1_2'),
    path('tabela2/', ask_known2_view2, name='ask_known2_2'),
    path('tabela3/', process_values_view2, name='process_values_2'),
    
    path('error-value2/', error_value_view2, name='error_value_2'),
    
    # CORREÇÃO CRÍTICA: 
    # 1. A view é error_type_view7 (definida no views2.py anterior).
    # 2. O name='error_type_7' é obrigatório pois o views2.py faz: redirect('error_type_7').
    path('error-type2/', error_type_view7, name='error_type_7'),
]