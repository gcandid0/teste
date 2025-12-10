from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('myapp.cilindro_urls')),  # Inclui as URLs do aplicativo myapp
    path('', include('myapp.tabela_urls')),  # Inclui as URLs do aplicativo myapp
    path('admin/', admin.site.urls),
    path('cilindro/', include('myapp.cilindro_urls')),  # Inclui as URLs específicas para "cilindro/"
    path('tabela/', include('myapp.tabela_urls')),      # Inclui as URLs específicas para "tabela/"
    path('gas/', include('myapp.gas_urls')),  
]

# Redirecionamentos para as páginas iniciais
urlpatterns += [
    path('', RedirectView.as_view(url='/cilindro/')),  # Redireciona a página inicial para "cilindro/"
    path('', RedirectView.as_view(url='/tabela/')),  # Redireciona a página inicial para "cilindro/"
]
