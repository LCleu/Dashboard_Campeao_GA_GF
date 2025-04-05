import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from dash.dependencies import State
import plotly.graph_objects as go
import xlrd # Importa a biblioteca xlrd para ler arquivos Excel   
import openpyxl # Importa a biblioteca openpyxl para ler arquivos Excel
import random

# Dicionário com os links exatos dos escudos
club_logos = {
    "Flamengo": "/assets/fla.png",
    "América (MG)": "/assets/amemi.png",
    "Atlético Goianiense": "/assets/ago.png",
    "Atlético Madrid": "/assets/ama.png",
    "Atlético Mineiro": "/assets/ami.png",
    "Barcelona": "/assets/bar.png",
    "Bayern Munich": "/assets/bay.png",
    "Botafogo (RJ)": "/assets/fogo.png",
    "Bragantino": "/assets/rbb.png",
    "Chapecoense": "/assets/chap.png",
    "Chelsea": "/assets/chel.png",
    "Corinthians": "/assets/cor.png",
    "Cruzeiro": "/assets/cru.png",
    "Fortaleza": "/assets/for.png",
    "Inter": "/assets/int.png",
    "Joinville": "/assets/joi.png",
    "Juventus": "/assets/juv.png",
    "Leicester City": "/assets/lei.png",
    "Leverkusen": "/assets/lever.png",
    "Lille": "/assets/lil.png",
    "Liverpool": "/assets/liv.png",
    "Manchester City": "/assets/cit.png",
    "Milan": "/assets/mil.png",
    "Monaco": "/assets/monaco.png",
    "Napoli": "/assets/nap.png",
    "Palmeiras": "/assets/pal.png",
    "Paris S-G": "/assets/psg.png",
    "Real Madrid": "/assets/real.png",
    "Santos": "/assets/san.png",
    "Vitória": "/assets/vit.png"
}

  


# Carrega os dados
df = pd.read_excel('Base_de_dados_big5_e_BR.xlsx', sheet_name='Página1')
df.columns = df.columns.str.strip()
df['Melhor'] = df['Melhor'].str.strip()
df['Campeonato'] = df['Campeonato'].str.strip()

leagues = df['Campeonato'].dropna().unique()
performance_types = ['Ataque', 'Defesa', 'Ataque e Defesa', '0']

app = Dash(__name__)
server = app.server

def generate_league_checklist(league_name):
    return html.Div([
        html.H4(league_name),
        dcc.Checklist(
            id=f'checklist-master-{league_name}',
            options=[{'label': 'Selecionar todos', 'value': 'all'}],
            value=['all'],
            labelStyle={'fontWeight': 'bold'}
        ),
        dcc.Checklist(
            id=f'checklist-{league_name}',
            options=[
                {'label': 'Melhor Ataque', 'value': 'Ataque'},
                {'label': 'Melhor Defesa', 'value': 'Defesa'},
                {'label': 'Melhor Ataque e Defesa', 'value': 'Ataque e Defesa'},
                {'label': 'Não teve destaques', 'value': '0'}
            ],
            value=['Ataque', 'Defesa', 'Ataque e Defesa', '0'],
            labelStyle={'display': 'block'}
        )
    ], style={'margin-bottom': '20px'})

app.layout = html.Div([
    html.H1('Gráfico de Gols Marcados vs Gols Sofridos - Campeões'),
    html.Div(
        children=[
            html.Div(generate_league_checklist(league), style={'flex': '1', 'min-width': '150px'}) 
            for league in leagues
        ],
        style={'display': 'flex', 'justify-content': 'space-evenly', 'flex-wrap': 'wrap'}
    ),
    dcc.Graph(id='scatter-graph')
])

@app.callback(
    Output('scatter-graph', 'figure'),
    [Input(f'checklist-{league}', 'value') for league in leagues]
)



def update_graph(*selected_performances):
    filtered_df = pd.DataFrame()

    for i, league in enumerate(leagues):
        perf_list = selected_performances[i]
        if perf_list:
            filtered = df[(df['Campeonato'] == league) & (df['Melhor'].isin(perf_list))]
            filtered_df = pd.concat([filtered_df, filtered])

    fig = go.Figure()
    for _, row in filtered_df.iterrows():
        club = row['Squad']
        logo_url = club_logos.get(club)
        year = row.get('Year', 'Unknown')  # Ensure 'Year' exists in your DataFrame
        top_scorer = row.get('Top Scorer', 'Unknown')  # Ensure 'Top Scorer' exists in your DataFrame
        GA = int(row.get('GA', 0))  # Ensure 'GA' exists in your DataFrame
        GF = int(row.get('GF', 0))  # Ensure 'GF' exists in your DataFrame
        if logo_url:
            ofset = random.uniform(-0.6, 0.6)  # Random offset for x position
            fig.add_layout_image(
                dict(
                    source=logo_url,
                    x=row['GA']+(ofset),  
                    y=row['GF'],  
                    xref="x",
                    yref="y",
                    sizex=5.5,
                    sizey=5.5,
                    opacity=1,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
                )
            )
            # Add a scatter point for hover information
            fig.add_trace(go.Scatter(
                x=[row['GA']+(ofset)],
                y=[row['GF']],
                mode='markers',
                marker=dict(size=1, opacity=0),
                hovertemplate=(
                    f"<b>{club}</b><br>"
                    f"Year: {year}<br>"
                    f"Top Scorer: {top_scorer}<br>"
                    f"Gols Sofridos (GA): {GA}<br>"
                    f"Gols Marcados (GF): {GF}<extra></extra>"
                )
            ))

    fig.update_layout(
        title='Gols Marcados (GF) vs Gols Sofridos (GA)',
        xaxis_title='Gols Sofridos',
        yaxis_title='Gols Marcados',
        xaxis=dict(range=[df['GA'].min()-5, df['GA'].max()+5]),
        yaxis=dict(range=[df['GF'].min()-5, df['GF'].max()+5]),
        height=700
    )

    return fig
    filtered_df = pd.DataFrame()

    for i, league in enumerate(leagues):
        perf_list = selected_performances[i]
        if perf_list:
            filtered = df[(df['Campeonato'] == league) & (df['Melhor'].isin(perf_list))]
            filtered_df = pd.concat([filtered_df, filtered])

    fig = go.Figure()
    for _, row in filtered_df.iterrows():
        club = row['Squad']
        logo_url = club_logos.get(club)
        if logo_url:
            fig.add_layout_image(
                dict(
                    source=logo_url,
                    x=row['GA'],
                    y=row['GF'],
                    xref="x",
                    yref="y",
                    sizex=5.5,
                    sizey=5.5,
                    xanchor="center",
                    yanchor="middle",
                    layer="above"
                )
            )

    fig.update_layout(
        title='Gols Marcados (GF) vs Gols Sofridos (GA)',
        xaxis_title='Gols Sofridos',
        yaxis_title='Gols Marcados',
        xaxis=dict(range=[df['GA'].min()-2, df['GA'].max()+2]),
        yaxis=dict(range=[df['GF'].min()-2, df['GF'].max()+2]),
        height=700
    )

    return fig

for league in leagues:
    @app.callback(
        Output(f'checklist-{league}', 'value'),
        Input(f'checklist-master-{league}', 'value'),
        State(f'checklist-{league}', 'options'),
        prevent_initial_call=True
    )
    def select_all(master_value, options):
        all_values = [opt['value'] for opt in options]
        return all_values if 'all' in master_value else []

if __name__ == '__main__':
    app.run(debug=True)
