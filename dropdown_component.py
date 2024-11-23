from dash import dcc, html

def create_dropdown():
    """Retorna o layout do dropdown."""
    return html.Div([
        html.Label("Selecione o gráfico:"),
        dcc.Dropdown(
            id="dropdown-graficos",
            options=[
                {"label": "Distribuição de Avaliações", "value": "histogram_rating"},
                {"label": "Número de Votos por Ano", "value": "votes_by_year"},
                {"label": "Gêneros Mais Populares", "value": "popular_genres"},
                {"label": "Correlação: Avaliação x Votos", "value": "rating_vs_votes"},
                {"label": "Quantidade por Tipo", "value": "count_by_type"}
            ],
            value=None,
            clearable=True,
            placeholder="Selecione um gráfico"
        )
    ])
