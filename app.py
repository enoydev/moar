import dash
from dash import dcc, html, Input, Output, State
from upload_component import create_upload_component, parse_contents
from dropdown_component import create_dropdown
from graph_functions import create_graph
import os
import plotly.express as px
import logging
from insights import insight

# Configurar logs
logging.basicConfig(level=logging.INFO)

# Inicializar o app Dash
app = dash.Dash(__name__)
app.title = "REBYTE"

# Holder do DataFrame global
df_global = None

# Layout principal
app.layout = html.Div([
    html.H1("REBYTE"),
    create_upload_component(),
    create_dropdown(),
    dcc.Loading(
        id="loading-grafico",
        type="circle",
        children=dcc.Graph(id="grafico-selecionado"),
        style={"margin-top": "20px"}
    ),
    html.Button("Gerar Insight", id="botao-grafico", n_clicks=0),
    dcc.Loading(
        id="loading-insight",
        type="circle",
        children=html.Div(id="mensagem-botao"),
        style={"margin-top": "20px"}
    ),
])

# Callback para processar o upload
@app.callback(
    [Output("upload-status", "children"),
     Output("data-table", "data"),
     Output("data-table", "columns")],
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def processar_upload(contents, filename):
    global df_global
    if contents is not None:
        df_global = parse_contents(contents, filename)
        if df_global is not None:
            columns = [{"name": col, "id": col} for col in df_global.columns]
            data = df_global.to_dict("records")
            return (
                html.Div(
                    f"Arquivo '{filename}' carregado com sucesso!",
                    className="success-message"
                ),
                data,
                columns
            )
        return (
             html.Div(
                "Erro ao carregar o arquivo. Certifique-se de que é um CSV válido.",
                className="error-message"
            ),
            [], []
        )
    return "Nenhum arquivo carregado ainda.", [], []

# Callback para atualizar o gráfico
@app.callback(
    Output("grafico-selecionado", "figure"),
    [Input("dropdown-graficos", "value")],
)
def atualizar_grafico(tipo_grafico):
    global df_global
    grafico_vazio = px.scatter(title="Nenhum gráfico disponível")
    if df_global is not None and tipo_grafico:
        return create_graph(tipo_grafico, df_global)
    return grafico_vazio

# Callback para gerar o insight
@app.callback(
    Output("mensagem-botao", "children"),
    Input("botao-grafico", "n_clicks"),
    State("dropdown-graficos", "value")
)
def gerar_insight(n_clicks, tipo_grafico):
    if n_clicks > 0:
        if tipo_grafico and df_global is not None:
            #baixando grafico
            fig = create_graph(tipo_grafico, df_global)
            file_path = os.path.join(os.getcwd(), "img.png")
            logging.info(f"Salvando gráfico em {file_path}")
            fig.write_image(file_path)
            logging.info("Gráfico salvo com sucesso.")
            
            ai_msg = insight()
            return html.Div([
                html.H4("Insight:"),
                html.P(ai_msg)
            ])
        return "Adicione o arquivo CSV e escolha um gráfico primeiro."
    return dash.no_update

# Inicializar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
