import plotly.express as px

def create_graph(graph_type, df):
    """Gera gráficos com base no tipo selecionado e no DataFrame."""
    if df is None or graph_type is None:
        return px.scatter(title="Nenhum gráfico disponível")

    if graph_type == "histogram_rating":
        fig = px.histogram(df, x="averageRating", nbins=20, title="Distribuição de Avaliações")
    elif graph_type == "votes_by_year":
        df_filtered = df.groupby("releaseYear")["numVotes"].sum().reset_index()
        fig = px.bar(df_filtered, x="releaseYear", y="numVotes", title="Número de Votos por Ano")
    elif graph_type == "popular_genres":
        df_genres = df["genres"].str.split(",").explode().value_counts().reset_index()
        df_genres.columns = ["Genre", "Count"]
        fig = px.bar(df_genres, x="Genre", y="Count", title="Gêneros Mais Populares")
    elif graph_type == "rating_vs_votes":
        fig = px.scatter(df, x="averageRating", y="numVotes", title="Relação: Avaliação x Votos")
    elif graph_type == "count_by_type":
        fig = px.bar(df["type"].value_counts().reset_index(), x="index", y="type",
                     labels={"index": "Type", "type": "Count"}, title="Quantidade por Tipo")
    else:
        fig = px.scatter(title="Nenhum gráfico selecionado")

    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig
