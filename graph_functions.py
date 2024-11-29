import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go

#GASTOS
categorias1 = ['Impostos e Encargos', 'Serviços Públicos', 'Serviços Terceirizados', 'Folha de Pagamento']

#SERVIÇOS
categorias2 = [
    "Climatização Residencial e Comercial",
    "Assistência Técnica para Eletrodomésticos",
    "Linha Branca - Venda e Manutenção",
    "Serviços de Informática",
    "Manutenção Preventiva e Corretiva",
    "Vendas de Equipamentos e Peças",
    "Consultoria Técnica e Perícia"
]


def create_graph(graph_type, df):
    """
    Gera gráficos com base no tipo selecionado e no DataFrame fornecido.

    Parâmetros:
        graph_type (str): O tipo de gráfico a ser gerado.
        df (pd.DataFrame): O DataFrame contendo os dados para o gráfico.

    Retorna:
        plotly.graph_objects.Figure: O gráfico gerado.
    """
    if df is None or graph_type is None:
        return px.scatter(title="Nenhum gráfico disponível")

    if graph_type == "distribuicao_valores":
        # Gráfico de distribuição de valores (histograma)
        fig = px.histogram(df, x="valor", nbins=20,
                           title="Distribuição dos Valores",
                           labels={"valor": "Valor"})
    elif graph_type == "total_por_categoria":
        # Gráfico total por categoria (barras)
        distribuicao_categorias = df.groupby('categoria')['valor'].sum().reset_index()
        fig = px.bar(distribuicao_categorias, x="categoria", y="valor",
                     title="Total por Categoria",
                     labels={"categoria": "Categoria", "valor": "Valor Total"})
    elif graph_type == "frequencia_status":
        # Gráfico de frequência de status (barras)
        frequencia_status = df['status'].value_counts().reset_index()
        frequencia_status.columns = ["Status", "Quantidade"]
        fig = px.bar(frequencia_status, x="Status", y="Quantidade",
                     title="Frequência por Status de Pagamento")
    elif graph_type == "distribuicao_temporal":
        # Gráfico de distribuição temporal (linha)

        faturamento = df[
            (df['status'] == 'PG') & (df['categoria'].isin(categorias2))
            ].groupby(['data', 'categoria'])['valor'].sum().reset_index()

        gastos = df[
            (df['status'] == 'PG') & (df['categoria'].isin(categorias1))
            ].groupby(['data', 'categoria'])['valor'].sum().reset_index()

        # Criando o DataFrame de comparação
        comparacao = pd.DataFrame({
            'faturamento': faturamento.groupby('data')['valor'].sum(),
            'gastos': gastos.groupby('data')['valor'].sum(),
        }).reset_index()

        # Extraindo apenas o ano como string ou inteiro
        comparacao['ano'] = comparacao['data'].str[:4]  # Assume que 'data' está no formato 'YYYY-MM-DD'

        # Agrupando novamente pelos anos
        comparacao_ano = comparacao.groupby('ano').sum().reset_index()

        # Tratando os dados
        comparacao_ano['faturamento'] = pd.to_numeric(comparacao_ano['faturamento'], errors='coerce').fillna(0)
        comparacao_ano['gastos'] = pd.to_numeric(comparacao_ano['gastos'], errors='coerce').fillna(0)
        comparacao_ano['saldo'] = comparacao_ano['faturamento'] - comparacao_ano['gastos']

        # Criação do gráfico
        fig = go.Figure()

        # Adicionando a linha de faturamento
        fig.add_trace(go.Scatter(
            x=comparacao_ano['ano'],
            y=comparacao_ano['faturamento'],
            mode='lines+markers',
            name='Faturamento',
            line=dict(color='green'),
            marker=dict(symbol='circle')
        ))

        # Adicionando a linha de gastos
        fig.add_trace(go.Scatter(
            x=comparacao_ano['ano'],
            y=comparacao_ano['gastos'],
            mode='lines+markers',
            name='Gastos',
            line=dict(color='red'),
            marker=dict(symbol='circle')
        ))

        # Preenchendo a área entre as linhas
        fig.add_trace(go.Scatter(
            x=comparacao_ano['ano'],
            y=comparacao_ano['faturamento'],
            mode='none',
            fill='tonexty',
            fillcolor='rgba(0, 255, 0, 0.3)',
            name='Lucro',
            showlegend=False,
            hoverinfo='none',
            visible='legendonly'
        ))

        # Atualizando layout
        fig.update_layout(
            title='Comparação de Faturamento e Gastos por Ano',
            xaxis_title='Ano',
            yaxis_title='Valores',
            template='plotly_white'
        )



    else:
        # Caso o tipo de gráfico não seja reconhecido
        fig = px.scatter(title="Nenhum gráfico selecionado")

    # Configurações de layout
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
