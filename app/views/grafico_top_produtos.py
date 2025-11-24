import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.http import HttpResponse


def grafico_top_produtos(request):
    caminho_csv = '/home/gedson/Documents/github/djangoproject/app/data/vendas_2024_completas.csv'

    df = pd.read_csv(caminho_csv)

    top_produtos = (
        df.groupby('produto')['quantidade'].sum().sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    top_produtos.plot(kind='bar')
    ax.set_title("Produtos Vendidos em 2024")
    ax.set_xlabel("Produto")
    ax.set_ylabel("Quantidade Vendida")
    ax.set_xticks(range(len(top_produtos.index)))
    ax.set_xticklabels(top_produtos.index, rotation=45, ha='right')


    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
    