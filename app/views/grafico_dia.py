from django.shortcuts import render
import pandas as pd
import plotly.express as px
from prophet import Prophet
import os
from django.conf import settings


def grafico_vendas_interativo(request):
    # Caminho do CSV
    caminho_csv = os.path.join(settings.BASE_DIR, "app", "data", "vendas_2024_completas.csv")

    # ====== CARREGAR E PREPARAR DADOS ======
    df = pd.read_csv(caminho_csv)
    df['data'] = pd.to_datetime(df['data'], format="%Y-%m-%d", errors='coerce')
    df = df.sort_values("data")

    # Agrupar vendas diárias para alimentar o Prophet
    vendas_diarias = df.groupby('data')['quantidade'].sum().reset_index()
    prophet_df = vendas_diarias.rename(columns={'data': 'ds', 'quantidade': 'y'})

    # ====== TREINAR PROPHET ======
    modelo = Prophet()
    modelo.fit(prophet_df)

    # Criar datas futuras mas LIMITANDO ATÉ 31/12/2025
    futuro = modelo.make_future_dataframe(periods=365)
    futuro = futuro[futuro['ds'] <= '2025-12-31']

    # Previsão
    forecast = modelo.predict(futuro)

    # Previsão somente a partir da última data real e antes de 2026
    ultima_data = df['data'].max()
    forecast = forecast[
        (forecast['ds'] > ultima_data) &
        (forecast['ds'] <= '2025-12-31')
    ]

    # Previsão diária formatada
    previsao_diaria = forecast[['ds', 'yhat']].rename(columns={'ds': 'data', 'yhat': 'previsao'})

    # ====== GRÁFICO DIÁRIO ======
    historico_diario = vendas_diarias.rename(columns={'quantidade': 'historico'})

    df_dia = pd.concat([
        historico_diario[['data', 'historico']],
        previsao_diaria[['data', 'previsao']]
    ], ignore_index=True)

    fig_dia = px.line(
        df_dia,
        x="data",
        y=["historico", "previsao"],
        labels={"value": "Quantidade", "variable": "Série"},
        title="Vendas Diárias: Histórico 2024 + Previsão 2025"
    )
    grafico_dia_html = fig_dia.to_html(full_html=False)

        # ====== GRÁFICO MENSAL ======
    # Histórico mensal
    df['mes'] = df['data'].dt.to_period('M').dt.to_timestamp()
    vendas_mensais = df.groupby('mes')['quantidade'].sum().reset_index()
    vendas_mensais.rename(columns={'quantidade': 'historico'}, inplace=True)
    vendas_mensais['mes_nome'] = vendas_mensais['mes'].dt.strftime("%b")

    # Previsão mensal
    previsao_diaria['mes'] = previsao_diaria['data'].dt.to_period('M').dt.to_timestamp()
    previsao_mensal = previsao_diaria.groupby('mes')['previsao'].sum().reset_index()
    previsao_mensal = previsao_mensal[previsao_mensal['mes'] <= '2025-12-01']
    previsao_mensal['mes_nome'] = previsao_mensal['mes'].dt.strftime("%b")

    # Combinar
    df_mes = pd.concat([
        vendas_mensais[['mes_nome', 'historico']],
        previsao_mensal[['mes_nome', 'previsao']]
    ], ignore_index=True)

    fig_mes = px.line(
        df_mes,
        x="mes_nome",
        y=["historico", "previsao"],
        labels={"value": "Quantidade", "variable": "Série", "mes_nome": "Mês"},
        title="Vendas Mensais: Histórico x Previsão (Comparação mês a mês)"
    )

    grafico_mes_html = fig_mes.to_html(full_html=False)

    # ====== RENDERIZAR NO HTML ======
    return render(request, "grafico_interativo.html", {
        "grafico_dia": grafico_dia_html,
        "grafico_mes": grafico_mes_html,
    })
