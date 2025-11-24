import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse


def grafico_top_canais(request):
    caminho_csv = '/home/gedson/Documents/github/djangoproject/app/data/vendas_2024_completas.csv'

    df = pd.read_csv(caminho_csv)

    top_canais = (
        df.groupby('canal')['quantidade'].sum().sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    top_canais.plot(kind='bar')
    ax.set_title("Vendas por Canal 2024")
    ax.set_xlabel("Canal")
    ax.set_ylabel("Quantidade Vendida")
    ax.set_xticks(range(len(top_canais.index)))
    ax.set_xticklabels(top_canais.index, rotation=45, ha='right')


    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
    
