import dash
from dash import dcc, html, Input, Output, State
from upload_component import create_upload_component, parse_contents
from dropdown_component import create_dropdown
from graph_functions import create_graph
import pandas as pd


app = dash.Dash(__name__)
app.title = "Dashboard Modularizado"

# holder do dataframe
df_global = None

# Layout principal
app.layout = html.Div([
    html.H1("Dashboard IMDb", style={'text-align': 'center'}),
    create_upload_component(),
    create_dropdown(),
    dcc.Graph(id="grafico-selecionado")
])

# callback p upload e atualizar taabela
@app.callback(
    [Output("upload-status", "children"),
     Output("data-table", "data"),
     Output("data-table", "columns")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def atualizar_dataset(contents, filename):
    global df_global
    if contents is not None:
        df_global = parse_contents(contents, filename)
        if df_global is not None:
            columns = [{"name": col, "id": col} for col in df_global.columns]
            data = df_global.to_dict("records")
            return f"Arquivo '{filename}' carregado com sucesso!", data, columns
        else:
            return "Erro ao carregar o arquivo. Certifique-se de que é um CSV.", [], []
    return "Nenhum arquivo carregado ainda.", [], []



# callback da atualização de leve do gráfico
@app.callback(
    Output("grafico-selecionado", "figure"),
    Input("dropdown-graficos", "value")
)
def atualizar_grafico(tipo_grafico):
    global df_global
    return create_graph(tipo_grafico, df_global)


if __name__ == "__main__":
    app.run_server(debug=True)
