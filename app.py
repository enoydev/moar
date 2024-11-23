import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Configurações iniciais do app
app = dash.Dash(__name__)

# Exemplo de dados para visualização
df = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D"],
    "Valores": [450, 250, 300, 500]
})

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard Básico com Dash", style={'text-align': 'center'}),

    # Dropdown para selecionar uma categoria (apenas exemplo)
    dcc.Dropdown(id="selecao-categoria",
                 options=[{"label": cat, "value": cat} for cat in df['Categoria']],
                 value="A",
                 style={'width': "40%"}),

    # Gráfico
    dcc.Graph(id="grafico-exemplo", figure={})
])

# Callback para atualizar o gráfico com base na seleção
@app.callback(
    Output(component_id="grafico-exemplo", component_property="figure"),
    [Input(component_id="selecao-categoria", component_property="value")]
)
def atualizar_grafico(categoria_selecionada):
    # Filtra os dados e cria um gráfico simples de barras
    df_filtrado = df[df["Categoria"] == categoria_selecionada]
    fig = px.bar(df_filtrado, x="Categoria", y="Valores", title=f"Valores para {categoria_selecionada}")
    return fig

# Rodar o servidor do dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
