# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('vendas.csv')

# Initialize the app
app = Dash()

# App layout (wrap in Div)
app.layout = html.Div([
    html.H1(children='Relatório de Vendas de Pão na Semana'),

    # Tabela de dados
    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=7,  # 7 dias da semana
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'}
    ),

    # Gráfico de barras - quantidade vendida por dia
    dcc.Graph(
        figure=px.bar(
            df,
            x='dia_semana',
            y='quantidade',
            title='Quantidade de Pães Vendidos por Dia',
            text_auto=True
        )
    ),

    # Gráfico de linha - receita ao longo da semana
    dcc.Graph(
        figure=px.line(
            df,
            x='dia_semana',
            y='receita_total',
            markers=True,
            title='Receita Total por Dia da Semana'
        )
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
