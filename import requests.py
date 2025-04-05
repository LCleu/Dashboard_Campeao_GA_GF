import pandas as pd
# Importa a biblioteca pandas, usada para manipular dados em formato de tabela (DataFrames)
import pandas as pd
# Importa o Plotly Express, usado para criar gráficos interativos de forma simples
import plotly.express as px
# Importa componentes do Dash para construir a aplicação web interativa
from dash import Dash, dcc, html, Input, Output

# Carrega o arquivo CSV contendo os dados dos campeões em um DataFrame
df = pd.read_csv("Base_de_dados_big5_e_BR - Página1.csv")  # Substitua "your_file.csv" pelo nome do seu arquivo CSV

# Inicializa o aplicativo Dash
app = Dash(__name__)

# Cria uma lista com os nomes únicos dos campeonatos disponíveis no dataset (ex: Premier League, Brasileirão, etc.)
leagues = sorted(df["Campeonato"].unique())

# Define os possíveis tipos de desempenho (valores encontrados na coluna "Melhor")
performance_types = ['0', 'Ataque', 'Defesa', 'Ataque e Defesa']

# Define o layout da aplicação Dash (a "interface" do usuário)
app.layout = html.Div([

    # Título principal da página
    html.H1("Campeões: Gols Marcados vs Gols Sofridos"),

    # Cria um dropdown para selecionar o campeonato (liga)
    html.Div([
        html.Label("Selecione o Campeonato:"),
        dcc.Dropdown(
            id='league-dropdown',  # ID que será usado no callback
            options=[    {'label': 'Premier League', 'value': 'Premier League'},
    {'label': 'La Liga', 'value': 'La Liga'},
    {'label': 'Serie A', 'value': 'Serie A'},
    {'label': 'Bundesliga', 'value': 'Bundesliga'},
    {'label': 'Ligue 1', 'value': 'Ligue 1'},
    {'label': 'Brasileirão', 'value': 'Brasileirão'}],  # Cria opções a partir dos nomes das ligas
            value=leagues[0],  # Define o valor padrão como a primeira liga da lista
            multi=True  # Só permite selecionar uma liga por vez
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),  # Define o estilo do dropdown (largura de 48%)

    # Cria outro dropdown para selecionar o tipo de desempenho ("Melhor")
    html.Div([
        html.Label("Tipo de Desempenho:"),
        dcc.Dropdown(
            id='performance-dropdown',  # ID que será usado no callback
            options=[    {'label': 'Nenhum Destaque', 'value': '0'},
    {'label': 'Melhor Ataque', 'value': 'Ataque'},
    {'label': 'Melhor Defesa', 'value': 'Defesa'},
    {'label': 'Melhor Ataque e Defesa', 'value': 'Ataque e Defesa'}],  # Cria opções com base nos valores únicos
            value='0',  # Define valor padrão como '0' (nenhum destaque)
            multi=True  # Só permite selecionar um tipo de desempenho por vez
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),  # Define o estilo do dropdown

    # Componente onde o gráfico será exibido
    dcc.Graph(id='scatter-plot')  # Este ID será usado no callback para atualizar o gráfico
])

# Define o callback que atualiza o gráfico com base nas seleções dos dois dropdowns
@app.callback(
    Output('scatter-plot', 'figure'),  # O output será o gráfico com ID 'scatter-plot'
    Input('league-dropdown', 'value'),  # Input 1: valor selecionado no dropdown da liga
    Input('performance-dropdown', 'value')  # Input 2: valor selecionado no dropdown de desempenho
)
def update_graph(selected_league, selected_performance):
    # Filtra o DataFrame com base na liga e no tipo de desempenho selecionados
    filtered_df = df[
        (df['Campeonato'] == selected_league) & (df['Melhor'] == selected_performance)  # Filtra pelo tipo de desempenho escolhido
    ]

    # Cria um gráfico de dispersão (scatter plot) com Plotly
    fig = px.scatter(
        filtered_df,  # Usa o DataFrame filtrado
        x='GA',  # Eixo X: Gols sofridos (Goals Against)
        y='GF',  # Eixo Y: Gols marcados (Goals For)
        text='Squad',  # Nome do time aparecerá no gráfico
        color='Squad',  # Cor por time, ajuda a identificar visualmente
        labels={'GA': 'Gols Sofridos', 'GF': 'Gols Marcados'},  # Rótulos personalizados para os eixos
        title=f'Gols Marcados vs Gols Sofridos - {selected_league} ({selected_performance})'  # Título do gráfico
    )

    # Ajusta a posição dos textos (nomes dos times) no gráfico
    fig.update_traces(textposition='top center')

    # Adiciona uma transição suave ao atualizar o gráfico
    fig.update_layout(transition_duration=500)

    # Retorna o gráfico atualizado
    return fig

# Inicia o servidor da aplicação quando o script for executado
if __name__ == '__main__':
    app.run(debug=True)
