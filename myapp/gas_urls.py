from django.urls import path
from .views6 import (
    ask_known1_view6, ask_known2_view6, ask_known3_view6,
    process_values_view6, gasideal_view, homepage_view, processosgasideal_view
)
from .views7 import (
    ask_known1_view7, ask_known2_view7, ask_known3_view7,
    process_values_view7, error_type_view7
)
from .views8 import (
    ask_known1_view8, ask_known2_view8, ask_known3_view8, ask_known4_view8,
    ask_known5_view8, ask_known6_view8, 
    process_values_view8, error_type_view8
)
from .views9 import (
    ask_known1_view9, ask_known2_view9, ask_known3_view9, ask_known4_view9,
    ask_known5_view9, ask_known6_view9,
    process_values_view9, error_type_view9
)
from .views10 import (
    ask_known1_view10, ask_known2_view10, ask_known3_view10, ask_known4_view10,
    ask_known5_view10, ask_known6_view10,
    process_values_view10, error_type_view10
)
from .views11 import (
    ask_known1_view11, ask_known2_view11, ask_known3_view11, ask_known4_view11,
    ask_known5_view11, ask_known6_view11, ask_known7_view11,
    process_values_view11, error_type_view11
)

from .views12 import (
    ask_known1_view12, ask_known2_view12, ask_known3_view12, ask_known4_view12,
    ask_known5_view12, process_values_view12, error_type_view12
)

urlpatterns = [
    # Página inicial e seções principais
    path('', homepage_view, name='homepage'),
    path('gasideal/', gasideal_view, name='gasideal'),
    path('processos-gas/', processosgasideal_view, name='processos2'),

    # -----------------------------
    # SEÇÃO 6 – Gás Ideal (Geral)
    # -----------------------------
    path('gasideal1/', ask_known3_view6, name='ask_known3_6'),
    path('gasideal2/', ask_known1_view6, name='ask_known1_6'),
    path('gasideal3/', ask_known2_view6, name='ask_known2_6'),
    path('gasideal4/', process_values_view6, name='process_values_6'),

    # -----------------------------
    # SEÇÃO 7 – Gás Ideal no Cilindro
    # -----------------------------
    path('gasideal-cilindro1/', ask_known3_view7, name='ask_known3_7'),
    path('gasideal-cilindro2/', ask_known1_view7, name='ask_known1_7'),
    path('gasideal-cilindro3/', ask_known2_view7, name='ask_known2_7'),
    path('gasideal-cilindro4/', process_values_view7, name='process_values_7'),
    path('error-type7/', error_type_view7, name='error_type7'),

    # -----------------------------
    # SEÇÃO 8 – Pressão Constante
    # -----------------------------
    path('gasideal-pcte1/', ask_known1_view8, name='ask_known1_8'),
    path('gasideal-pcte2/', ask_known2_view8, name='ask_known2_8'),
    path('gasideal-pcte3/', ask_known3_view8, name='ask_known3_8'),
    path('gasideal-pcte4/', ask_known4_view8, name='ask_known4_8'),
    path('gasideal-pcte5/', ask_known5_view8, name='ask_known5_8'),
    path('gasideal-pcte6/', ask_known6_view8, name='ask_known6_8'),
    path('gasideal-pcte7/', process_values_view8, name='process_values_8'),
    path('error-type8/', error_type_view8, name='error_type8'),

    # -----------------------------
    # SEÇÃO 9 – Volume Constante
    # -----------------------------
    path('gasideal-vcte1/', ask_known1_view9, name='ask_known1_9'),
    path('gasideal-vcte2/', ask_known2_view9, name='ask_known2_9'),
    path('gasideal-vcte3/', ask_known3_view9, name='ask_known3_9'),
    path('gasideal-vcte4/', ask_known4_view9, name='ask_known4_9'),
    path('gasideal-vcte5/', ask_known5_view9, name='ask_known5_9'),
    path('gasideal-vcte6/', ask_known6_view9, name='ask_known6_9'),
    path('gasideal-vcte7/', process_values_view9, name='process_values_9'),
    path('error-type9/', error_type_view9, name='error_type9'),

    # -----------------------------
    # SEÇÃO 10 – Temperatura Constante (Isotérmico)
    # -----------------------------
    path('gasideal-tcte1/', ask_known1_view10, name='ask_known1_10'),
    path('gasideal-tcte2/', ask_known2_view10, name='ask_known2_10'),
    path('gasideal-tcte3/', ask_known3_view10, name='ask_known3_10'),
    path('gasideal-tcte4/', ask_known4_view10, name='ask_known4_10'),
    path('gasideal-tcte5/', ask_known5_view10, name='ask_known5_10'),
    path('gasideal-tcte6/', ask_known6_view10, name='ask_known6_10'),
    path('gasideal-tcte7/', process_values_view10, name='process_values_10'),
    path('error-type10/', error_type_view10, name='error_type10'),

    # -----------------------------
    # SEÇÃO 11 – Processo Politrópico
    # -----------------------------
    path('gasideal-poli1/', ask_known1_view11, name='ask_known1_11'),
    path('gasideal-poli2/', ask_known2_view11, name='ask_known2_11'),
    path('gasideal-poli3/', ask_known3_view11, name='ask_known3_11'),
    path('gasideal-poli4/', ask_known4_view11, name='ask_known4_11'),
    path('gasideal-poli5/', ask_known5_view11, name='ask_known5_11'),
    path('gasideal-poli6/', ask_known6_view11, name='ask_known6_11'),
    path('gasideal-poli7/', ask_known7_view11, name='ask_known7_11'),
    path('gasideal-poli8/', process_values_view11, name='process_values_11'),
    path('error-type11/', error_type_view11, name='error_type11'),
    
        # -----------------------------
    # SEÇÃO 12 – Entropia Constante (Isentrópico)
    # -----------------------------
    path('gasideal-scte1/', ask_known1_view12, name='ask_known1_12'),
    path('gasideal-scte2/', ask_known2_view12, name='ask_known2_12'),
    path('gasideal-scte3/', ask_known3_view12, name='ask_known3_12'),
    path('gasideal-scte4/', ask_known4_view12, name='ask_known4_12'),
    path('gasideal-scte5/', ask_known5_view12, name='ask_known5_12'),
    path('gasideal-scte6/', process_values_view12, name='process_values_12'),
    path('error-type12/', error_type_view12, name='error_type12'),
    
]
