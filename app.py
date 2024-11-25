import dash
from dash import dcc, html, Input, Output, State
from upload_component import create_upload_component, parse_contents
from dropdown_component import create_dropdown
from graph_functions import create_graph
import os
import plotly.express as px
import logging
from datetime import datetime
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
    html.H1("REBYTE"),  # Estilo movido para style.css
    create_upload_component(),
    create_dropdown(),
    dcc.Graph(id="grafico-selecionado"),
    html.Button("Gerar Insight", id="botao-grafico", n_clicks=0),  # Estilo movido para style.css
    html.Div(id="mensagem-botao"),  # Apenas um ID "mensagem-botao"
    dcc.Loading(
        id="loading-insight",
        type="circle",  # Pode ser "circle", "default" ou "dot"
        children=html.Div(id="loading-mensagem-botao"),  # Alterado para "loading-mensagem-botao"
    ),
])

# Callback para upload, gráfico e botão
@app.callback(
    [Output("upload-status", "children"),
     Output("data-table", "data"),
     Output("data-table", "columns"),
     Output("grafico-selecionado", "figure"),
     Output("mensagem-botao", "children")],
    [Input("upload-data", "contents"),
     Input("botao-grafico", "n_clicks"),
     Input("dropdown-graficos", "value")],
    [State("upload-data", "filename")]
)
def atualizar_interface(contents, n_clicks_botao, tipo_grafico, filename):
    global df_global
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    mensagem_botao = ""
    grafico_vazio = px.scatter(title="Nenhum gráfico disponível")  # Gráfico vazio padrão

    try:
        if triggered_id == "upload-data":
            if contents is not None:
                df_global = parse_contents(contents, filename)
                if df_global is not None:
                    columns = [{"name": col, "id": col} for col in df_global.columns]
                    data = df_global.to_dict("records")
                    return (
                        f"Arquivo '{filename}' carregado com sucesso!",
                        data,
                        columns,
                        create_graph(tipo_grafico, df_global) if tipo_grafico else grafico_vazio,
                        mensagem_botao
                    )
                else:
                    return (
                        "Erro ao carregar o arquivo. Certifique-se de que é um CSV.",
                        [], 
                        [], 
                        grafico_vazio, 
                        mensagem_botao
                    )
            return "Nenhum arquivo carregado ainda.", [], [], grafico_vazio, mensagem_botao

        elif triggered_id == "botao-grafico":
            logging.info(f"Botão clicado {n_clicks_botao} vezes.")
            if n_clicks_botao > 0 and tipo_grafico and df_global is not None:
                fig = create_graph(tipo_grafico, df_global)
                #mensagem_botao = "Gráfico salvo com sucesso!"
                file_path = os.path.join(os.getcwd(), "img.png")
                
                logging.info(f"Salvando gráfico em {file_path}")
                fig.write_image(file_path)
                logging.info("Gráfico salvo com sucesso.")
                
                # Obtendo o insight
                ai_msg = insight()

                # Criando o conteúdo HTML com o insight sem a estilização
                insight_html = html.Div(
                    [
                        html.H4("Insight:"), 
                        html.P(ai_msg)
                    ]
                )

                # Combinando a mensagem do botão com o insight
                mensagem_botao = [insight_html]

                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    fig,
                    mensagem_botao
                )
            else:
                mensagem_botao = "Adicione o arquivo CSV primeiro."
                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    grafico_vazio,
                    mensagem_botao
                )

        elif triggered_id == "dropdown-graficos":
            fig = create_graph(tipo_grafico, df_global) if tipo_grafico else grafico_vazio
            return (
                dash.no_update,
                dash.no_update,
                dash.no_update,
                fig,
                mensagem_botao
            )

        return "Nenhum arquivo carregado ainda.", [], [], grafico_vazio, mensagem_botao

    except Exception as e:
        logging.error(f"Erro no callback: {e}")
        return (
            "Erro interno. Consulte os logs para mais informações.",
            [], 
            [], 
            grafico_vazio, 
            "Erro no processamento."
        )


if __name__ == "__main__":
    app.run_server(debug=True)
