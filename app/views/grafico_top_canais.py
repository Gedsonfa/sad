from django.shortcuts import render
import pandas as pd
import plotly.express as px
import os
from django.conf import settings

def grafico_top_canais(request):
    caminho_csv = os.path.join(settings.BASE_DIR, "app", "data", "vendas_2024_completas.csv")

    df = pd.read_csv(caminho_csv)

    # Agrupar por canal
    top_canais = (
        df.groupby('canal')['quantidade'].sum().reset_index()
    )

    # Criar gráfico de pizza com Plotly Express
    fig = px.pie(
        top_canais,
        names='canal',
        values='quantidade',
        title='Vendas por Canal - 2024',
        hole=0  # 0 = pizza normal / 0.4 = donut
    )

    # Converter para HTML
    grafico_html = fig.to_html(full_html=False)

    return render(request, "grafico_canais.html", {
        "grafico": grafico_html
    })
