from dash import dcc, html

def create_dropdown():
    """Retorna o layout do dropdown."""
    return html.Div([
        html.Label("Selecione o gráfico:"),
        dcc.Dropdown(
            id="dropdown-graficos",
            options=[
                {"label": "Distribuição dos Valores", "value": "distribuicao_valores"},
                {"label": "Total por Categoria", "value": "total_por_categoria"},
                {"label": "Frequência por Status", "value": "frequencia_status"},
                {"label": "Distribuição Temporal", "value": "distribuicao_temporal"}
            ],
            value=None,
            clearable=True,
            placeholder="Selecione um gráfico"
        )
    ])
