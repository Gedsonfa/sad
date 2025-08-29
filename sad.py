import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv('vendas.csv')

# Título do dashboard
st.title("Dashboard de Vendas de Pão na Semana")

# Exibir tabela
st.subheader("Tabela de Vendas")
st.dataframe(df)

# Gráfico de barras - quantidade vendida por dia
st.subheader("Quantidade de Pães Vendidos por Dia")
fig_bar = px.bar(
    df,
    x='dia_semana',
    y='quantidade',
    text='quantidade',
    title='Quantidade de Pães Vendidos por Dia'
)
st.plotly_chart(fig_bar)

# Gráfico de linha - receita ao longo da semana
st.subheader("Receita Total por Dia da Semana")
fig_line = px.line(
    df,
    x='dia_semana',
    y='receita_total',
    markers=True,
    title='Receita Total por Dia da Semana'
)
st.plotly_chart(fig_line)
