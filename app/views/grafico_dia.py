from django.shortcuts import render
import pandas as pd
import plotly.express as px
from prophet import Prophet

def grafico_vendas_interativo(request):
    caminho_csv = '/home/gedson/Documents/github/djangoproject/app/data/vendas_2024_completas.csv'

    df = pd.read_csv(caminho_csv)
    df['data'] = pd.to_datetime(df['data'], format="%Y-%m-%d", errors='coerce')
    df = df.sort_values("data")

    # ========================================
    # 1) PREPARE DADOS PARA O PROPHET
    # ========================================
    vendas_diarias = df.groupby('data')['quantidade'].sum().reset_index()
    prophet_df = vendas_diarias.rename(columns={'data': 'ds', 'quantidade': 'y'})

    modelo = Prophet()
    modelo.fit(prophet_df)

    # Previsão para 1 ano
    futuro = modelo.make_future_dataframe(periods=365)
    forecast = modelo.predict(futuro)

    # Apenas previsões de 2025 em diante
    forecast = forecast[forecast['ds'] > df['data'].max()]

    # Renomear previsões para concatenação
    previsao_diaria = forecast[['ds', 'yhat']].rename(columns={'ds': 'data', 'yhat': 'quantidade'})

    # ========================================
    # 2) GRÁFICO DIÁRIO (Histórico + Previsão)
    # ========================================
    # Histórico
    vendas_diarias.rename(columns={'quantidade': 'historico'}, inplace=True)

    # Unir histórico e previsão
    df_dia = pd.concat([vendas_diarias[['data', 'historico']], previsao_diaria], ignore_index=True)

    fig_dia = px.line(
        df_dia,
        x="data",
        y=["historico", "quantidade"],
        labels={"value": "Quantidade", "variable": "Série"},
        title="Vendas Diárias: Histórico 2024 + Previsão 2025"
    )
    grafico_dia_html = fig_dia.to_html(full_html=False)

    # ========================================
    # 3) GRÁFICO MENSAL (Histórico + Previsão)
    # ========================================
    # Mensal histórico
    df['mes'] = df['data'].dt.to_period('M').dt.to_timestamp()
    vendas_mensais = df.groupby('mes')['quantidade'].sum().reset_index()
    vendas_mensais.rename(columns={'quantidade': 'historico'}, inplace=True)

    # Mensal previsão
    previsao_diaria['mes'] = previsao_diaria['data'].dt.to_period('M').dt.to_timestamp()
    previsao_mensal = previsao_diaria.groupby('mes')['quantidade'].sum().reset_index()

    # Unir mensal histórico + previsão
    df_mes = pd.concat([vendas_mensais, previsao_mensal], ignore_index=True)

    fig_mes = px.line(
        df_mes,
        x="mes",
        y=["historico", "quantidade"],
        labels={"value": "Quantidade", "variable": "Série"},
        title="Vendas Mensais: Histórico 2024 + Previsão 2025"
    )
    grafico_mes_html = fig_mes.to_html(full_html=False)

    # ========================================
    # RENDERIZAR NO HTML
    # ========================================
    return render(request, "grafico_interativo.html", {
        "grafico_dia": grafico_dia_html,
        "grafico_mes": grafico_mes_html,
    })
