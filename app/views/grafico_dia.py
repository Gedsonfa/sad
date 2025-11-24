from django.http import HttpResponse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io


def grafico_vendas_diarias(request):
    caminho_csv = '/home/gedson/Documents/github/djangoproject/app/data/vendas_2024_completas.csv'

    df = pd.read_csv(caminho_csv)

    vendas_diarias = df.groupby('data')['quantidade'].sum()

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(vendas_diarias.index, vendas_diarias.values)
    ax.set_title("Vendas Diárias (Quantidade)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Quantidade")

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
    
