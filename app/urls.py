from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('grafico/vendas-diarias/', grafico_vendas_diarias, name='grafico_vendas_diarias'),
    path('grafico/top-produtos/', grafico_top_produtos, name='grafico_top_produtos'),
    path('grafico/top-canais/', grafico_top_canais, name='grafico_top_canais'),
]