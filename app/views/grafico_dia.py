from django.shortcuts import render
import pandas as pd
import plotly.express as px

def grafico_vendas_interativo(request):
    caminho_csv = '/home/gedson/Documents/github/djangoproject/app/data/vendas_2024_completas.csv'

    df = pd.read_csv(caminho_csv)
    df['data'] = pd.to_datetime(df['data'], format="%Y-%m-%d", errors='coerce')

    # ---- Gráfico Diário ----
    vendas_diarias = df.groupby('data')['quantidade'].sum().reset_index()

    fig_dia = px.line(
        vendas_diarias,
        x="data",
        y="quantidade",
        title="Vendas Diárias",
        markers=True
    )
    grafico_dia_html = fig_dia.to_html(full_html=False)

    # ---- Gráfico Mensal ----
    df['mes'] = df['data'].dt.to_period('M').dt.to_timestamp()
    vendas_mensais = df.groupby('mes')['quantidade'].sum().reset_index()

    fig_mes = px.line(
        vendas_mensais,
        x="mes",
        y="quantidade",
        title="Vendas Mensais",
        markers=True
    )
    grafico_mes_html = fig_mes.to_html(full_html=False)

    return render(request, "grafico_interativo.html", {
        "grafico_dia": grafico_dia_html,
        "grafico_mes": grafico_mes_html,
    })

