from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path("grafico/", grafico_vendas_interativo, name="grafico_vendas_interativo"),
    path('grafico/top-cidades/', grafico_top_cidades, name='grafico_top_cidades'),
    path('grafico/top-canais/', grafico_top_canais, name='grafico_top_canais'),
]