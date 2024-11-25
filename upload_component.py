import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import io
import base64

def create_upload_component():
    """Retorna o layout do componente de upload."""
    return html.Div([
        html.Label("Carregar Dataset:"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Arraste e solte ou ", html.A("selecione um arquivo")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=False  # Permitir apenas um arquivo por vez
        ),
        # Adicionando o indicador de loading ao status de upload
        dcc.Loading(
            id="loading-upload",
            overlay_style={"visibility":"visible", "filter": "blur(2px)"},
            type="circle",  # Você pode trocar para 'circle' ou 'dot'
            children=[
                html.Div(id="upload-status", style={"margin-top": "10px"}),
            ],
        ),
        dash_table.DataTable(
            id="data-table",
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                'minWidth': '100px',
                'width': '100px',
                'maxWidth': '180px',
                'whiteSpace': 'normal',
            },
        )
    ])

def parse_contents(contents, filename):
    """Processa o conteúdo do arquivo uploadado."""
    content_type, content_string = contents.split(',')
    decoded = io.BytesIO(base64.b64decode(content_string))
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(decoded)
            return df
        else:
            return None
    except Exception as e:
        print(e)
        return None
