import io
import dash
from dash import html, dcc, Input, Output, State, callback, callback_context
import pandas as pd
import io
import plotly.express as px
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/visualizacoes', name="Visualizações")
import json

layout = html.Div([

    html.Div([
        html.Div([
            html.Span("Extrator", style={'color': 'red', 'fontWeight': 'bold'}),
            html.Span("Lattes", style={'color': 'white', 'fontWeight': 'bold'})
        ], style={'display': 'inline-block', 'width': '50%', 'fontSize': '190%', 'fontFamily': 'Arial', 'padding': '20px'}),
        html.Div([
            html.Img(src='/assets/upe_logo_site.png', style={'width': '12%'})
        ], style={'display': 'inline-block', 'width': '50%', 'textAlign': 'right', 'padding': '10px'})
    ], style={'backgroundColor': '#001F3F', 'padding': '10px', 'display': 'flex'}),

    html.Div([
        html.Div([
            html.Div("Forma de visualização:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.Div([
                html.Button("Geral", id='btn-geral', n_clicks=0,
                            style={'padding': '10px 10px', 'backgroundColor': '#28a745', 'color': 'white',
                                   'border': 'none', 'borderRadius': '20px', 'margin': '5px', 'cursor': 'pointer',
                                   'boxShadow': '0px 2px 5px rgba(0,0,0,0.2)'}),
                html.Button("Por programa/grupo", id='btn-grupo', n_clicks=0,
                            style={'padding': '10px 10px', 'backgroundColor': '#28a745', 'color': 'white',
                                   'border': 'none', 'borderRadius': '20px', 'margin': '5px', 'cursor': 'pointer',
                                   'boxShadow': '0px 2px 5px rgba(0,0,0,0.2)'}),
                html.Button("Por Professor", id='btn-professor', n_clicks=0,
                            style={'padding': '10px 10px', 'backgroundColor': '#28a745', 'color': 'white',
                                   'border': 'none', 'borderRadius': '20px', 'margin': '5px', 'cursor': 'pointer',
                                   'boxShadow': '0px 2px 5px rgba(0,0,0,0.2)'})
            ], style={'display': 'flex', 'flexWrap': 'wrap'}),
html.Div([
    html.Div("Mediana: se refere à mediana da extração atual no modo escolhido.",
             style={
                 'fontStyle': 'italic',
                 'marginTop': '10px',
                 'fontSize': '12px',
                 'color': '#7f8c8d'
             }),
    html.Div(
        "Mediana Geral: se refere à mediana de todos os pesquisadores da UPE cadastrados no Sapiens. Extração feita em novembro de 2025, abordando o período de 2021 a 2025.",
        style={
            'fontStyle': 'italic',
            'fontSize': '12px',
            'color': '#7f8c8d'
        }),

    ]),
        ], style={'width': '45%', 'padding': '10px'}),

        html.Div([
            html.Div("Escolha as visualizações que deseja exibir:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Checklist(
                id='checklist-viz',
                options=[
                    {'label': 'Registros', 'value': 'registros'},
                    {'label': 'Orientações', 'value': 'orientacoes'},
                    {'label': 'Publicações', 'value': 'publicacoes'},
                    {'label': 'Outros', 'value': 'outros'},
                ],
                value=['registros', 'orientacoes', 'publicacoes', 'outros'],
                style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap', 'fontSize': '14px'}
            )
        ], style={'width': '45%', 'padding': '10px'}),

        html.Div([
            html.Button("Baixar Excel", id='btn-download', n_clicks=0,
                        style={'backgroundColor': '#28a745', 'color': 'white',
                               'padding': '10px 30px', 'fontSize': '16px',
                               'borderRadius': '20px', 'border': 'none', 'cursor': 'pointer'})
        ], style={'width': '20%', 'padding': '10px', 'textAlign': 'right', 'display': 'flex', 'alignItems': 'center'}),

    ], style={
        'display': 'flex',
        'backgroundColor': '#f4f4f4',
        'padding': '10px',
        'border': '1px solid #ddd',
        'borderRadius': '10px',
        'boxShadow': '0px 2px 6px rgba(0,0,0,0.1)',
        'marginBottom': '10px',
        'alignItems': 'center'
    }),

    html.Div(id="section-orientacoes", children=[
        html.H3("Orientações", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div([
            dcc.Checklist(id='check-mediana-orientacoes', options=[{'label': ' Exibir Medianas', 'value': 'SIM'}],
                          value=[],
                          style={'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '14px', 'color': '#2c3e50'})
        ]),
        html.Div(id="filtros-orientacoes-container"),
        html.Div(id="container-graficos",
                 style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'overflowX': 'auto',
                        'padding': '10px', 'gap': '15px', 'width': '100%', 'height': '450px'})
    ], style={"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
              "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%", "maxWidth": "1500px"}),

    html.Div(id="section-registros", children=[
        html.H3("Registros", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div([
            dcc.Checklist(id='check-mediana-registros', options=[{'label': ' Exibir Medianas', 'value': 'SIM'}],
                          value=[], style={'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '14px'})
        ]),
        html.Div(id="filtros-registros-container", children=[
            html.Div(id="wrapper-filtro-registros", style={'display': 'none'}, children=[
                html.Div([
                    html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Dropdown(id="filtro-grupo-registros", options=[], clearable=True,
                                 placeholder="Selecione o grupo")
                ], style={'width': '300px', 'display': 'flex', 'flexDirection': 'column', 'margin-left': '20px'})
            ])
        ]),
        html.Div(id="container-graficos-registros",
                 style={
                     'display': 'flex',
                     'flexDirection': 'row',
                     'overflowX': 'auto',
                     'padding': '20px',
                     'gap': '20px',
                     'width': '100%',
                     'alignItems': 'flex-start'
                 })
    ], style={"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
              "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%", "maxWidth": "1500px"}),

    # --- SEÇÃO PUBLICAÇÕES ---
    html.Div(id="section-publicacoes", children=[
        html.H3("Publicações", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div([
            dcc.Checklist(id='check-mediana-publicacoes', options=[{'label': ' Exibir Medianas', 'value': 'SIM'}],
                          value=[], style={'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '14px'})
        ]),
        html.Div(id="filtros-publicacoes-container", children=[
            html.Div(id="wrapper-filtro-publicacoes", style={'display': 'none'}, children=[
                html.Div([
                    html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Dropdown(id="filtro-grupo-publicacoes", options=[], clearable=True,
                                 placeholder="Selecione o grupo")
                ], style={'width': '300px', 'display': 'flex', 'flexDirection': 'column', 'margin-left': '20px'})
            ])
        ]),
        html.Div(id="container-graficos-publicacoes",
                 style={
                     'display': 'flex',
                     'flexDirection': 'row',
                     'overflowX': 'auto',
                     'padding': '20px',
                     'gap': '20px',
                     'width': '100%',
                     'alignItems': 'flex-start'
                 })
    ], style={"margin": "10px auto", "padding": "10px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
              "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%", "maxWidth": "1500px"}),

    # --- SEÇÃO OUTROS ---
    html.Div(id="section-outros", children=[
        html.H3("Outros", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div([
            dcc.Checklist(id='check-mediana-outros', options=[{'label': ' Exibir Medianas', 'value': 'SIM'}], value=[],
                          style={'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '14px'})
        ]),
        html.Div(id="filtros-outros-container", children=[
            html.Div(id="wrapper-filtro-outros", style={'display': 'none'}, children=[
                html.Div([
                    html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                    dcc.Dropdown(id="filtro-grupo-outros", options=[], clearable=True, placeholder="Selecione o grupo")
                ], style={'width': '300px', 'display': 'flex', 'flexDirection': 'column', 'margin-left': '20px'})
            ])
        ]),
        html.Div(id="container-graficos-outros",
                 style={
                     'display': 'flex',
                     'flexDirection': 'row',
                     'overflowX': 'auto',
                     'padding': '20px',
                     'gap': '20px',
                     'width': '100%',
                     'alignItems': 'flex-start'
                 })
    ], style={"margin": "10px auto", "padding": "10px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
              "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%", "maxWidth": "1500px"}),

    dcc.Download(id="download-dataframe-xlsx"),
    dcc.Store(id='store-modo-atual')
])

def ajustar_tamanho_grafico(df, min_barras=6, largura_por_barra=65, altura_por_barra=50,
                            largura_max=1000, altura_max=500, altura_min=350):
    n_barras = max(len(df), min_barras)
    largura = min(n_barras * largura_por_barra, largura_max)
    altura = max(min(n_barras * altura_por_barra, altura_max), altura_min)
    return f"{largura}px", f"{altura}px"

# Valores de referência para o cálculo da "Mediana Geral"
MEDIANAS_GERAIS = {
    # Orientações
    "mestrado": 0.0,
    "doutorado": 0.0,
    "ic": 0.0,
    "conc-esp": 0.0,
    "tcc-conc": 3.0,
    # Publicações
    "PUBLICAÇÕES CIENTÍFICAS": 4.0,
    "LIVROS ISBN": 0.0,
    "CAPÍTULOS ISBN": 1.0,
    "PUB. TRAB. EVENTOS": 0.0,
    # Registros
    "REGISTROS DE SW": 0.0,
    "PATENTES": 0.0,
    # Outros
    "EVENTOS ORGANIZADOS": 1.0,
    "PUB. TEC. E ART.": 0.0
}

def gerar_graficos_orientacoes(dfs, status, tipo, natureza, modo, metricas=None, exibir_mediana=False):
    colunas_map = {
        "mestrado": {"orientacoes": {"concluido": ["O.P MESTRADO CONC."], "andamento": ["O.P MESTRADO AND."]},
                     "coorientacoes": {"concluido": ["C.O MESTRADO CONC."], "andamento": ["C.O MESTRADO AND."]}},
        "doutorado": {"orientacoes": {"concluido": ["O.P DOUTORADO CONC."], "andamento": ["O.P DOUTORADO AND."]},
                      "coorientacoes": {"concluido": ["C.O DOUTORADO CONC."], "andamento": ["C.O DOUTORADO AND."]}},
        "ic": {"orientacoes": {"concluido": ["ORIENTAÇÕES I.C"], "andamento": []},
               "coorientacoes": {"concluido": [], "andamento": []}},
        "conc-esp": {"orientacoes": {"concluido": ["ORIENTACOES CONC. ESPECIALIZACAO"], "andamento": []},
                     "coorientacoes": {"concluido": [], "andamento": []}},
        "tcc-conc": {"orientacoes": {"concluido": ["ORIENTAÇÕES CONC. TCC"], "andamento": []},
                     "coorientacoes": {"concluido": [], "andamento": []}}
    }

    tipos_a_mostrar = list(colunas_map.keys()) if tipo == "todos" else [tipo]
    dados_plot = []

    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty: return []
        if 'Nome' in df_total.columns:
            df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]

        todas_metricas = ["O.P MESTRADO CONC.", "O.P MESTRADO AND.", "C.O MESTRADO CONC.", "C.O MESTRADO AND.",
                          "O.P DOUTORADO CONC.", "O.P DOUTORADO AND.", "C.O DOUTORADO CONC.", "C.O DOUTORADO AND.",
                          "ORIENTAÇÕES I.C", "ORIENTACOES CONC. ESPECIALIZACAO", "ORIENTAÇÕES CONC. TCC"]
        if metricas: todas_metricas = [c for c in todas_metricas if c in metricas]
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()

        for _, row in df_total.iterrows():
            professor = row['Nome']
            for t in tipos_a_mostrar:
                if natureza == "soma":
                    cols_conc = colunas_map[t]["orientacoes"]["concluido"] + colunas_map[t]["coorientacoes"]["concluido"]
                    cols_and = colunas_map[t]["orientacoes"]["andamento"] + colunas_map[t]["coorientacoes"]["andamento"]
                else:
                    cols_conc = colunas_map[t][natureza]["concluido"]
                    cols_and = colunas_map[t][natureza]["andamento"]
                val_conc = row[cols_conc].sum() if all(c in row.index for c in cols_conc) else 0
                val_and = row[cols_and].sum() if all(c in row.index for c in cols_and) else 0
                if status in ("concluido", "ambos"):
                    dados_plot.append({"Identificador": professor, "Tipo": t, "Status": "Concluído", "Valor": val_conc})
                if status in ("andamento", "ambos"):
                    dados_plot.append({"Identificador": professor, "Tipo": t, "Status": "Em andamento", "Valor": val_and})
    else:
        for grupo, df in dfs.items():
            for t in tipos_a_mostrar:
                if natureza == "soma":
                    cols_conc = colunas_map[t]["orientacoes"]["concluido"] + colunas_map[t]["coorientacoes"]["concluido"]
                    cols_and = colunas_map[t]["orientacoes"]["andamento"] + colunas_map[t]["coorientacoes"]["andamento"]
                else:
                    cols_conc = colunas_map[t][natureza]["concluido"]
                    cols_and = colunas_map[t][natureza]["andamento"]
                val_conc = df[cols_conc].sum(axis=1).sum() if cols_conc and all(c in df.columns for c in cols_conc) else 0
                val_and = df[cols_and].sum(axis=1).sum() if cols_and and all(c in df.columns for c in cols_and) else 0
                identificador = 'Total' if modo == 'geral' and grupo == 'total' else grupo
                if status in ("concluido", "ambos"):
                    dados_plot.append({"Identificador": identificador, "Tipo": t, "Status": "Concluído", "Valor": val_conc})
                if status in ("andamento", "ambos"):
                    dados_plot.append({"Identificador": identificador, "Tipo": t, "Status": "Em andamento", "Valor": val_and})

    df_plot = pd.DataFrame(dados_plot)
    graficos = []

    for t in tipos_a_mostrar:
        df_t = df_plot[df_plot["Tipo"] == t]
        if df_t.empty: continue
        ordem = df_t.groupby("Identificador")["Valor"].sum().sort_values(ascending=False).index.tolist()
        
        # No modo professor, renomear o eixo X para P1, P2, P3, etc. DEPOIS de ordenar
        if modo == 'professor':
            mapa_renomeacao = {ordem[i]: f'P{i+1}' for i in range(len(ordem))}
            df_t = df_t.copy()
            df_t['Identificador'] = df_t['Identificador'].map(mapa_renomeacao)
            ordem = [mapa_renomeacao[x] for x in ordem]
        
        fig = px.bar(df_t, x="Identificador", y="Valor", color="Status", barmode="stack", title=t.upper(), text_auto=True)

        # LÓGICA DE MEDIANA CONDICIONAL
        if exibir_mediana:
            try:
                sums = df_t.groupby("Identificador")["Valor"].sum()
                if len(sums) > 0 and modo != 'geral':
                    med_l = float(sums.median())
                    med_g = MEDIANAS_GERAIS.get(t, 0) if modo == 'professor' else None
                    if med_g is not None and med_l == med_g:
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana / Mediana Geral: {med_l:.1f}</b>",
                                      annotation_position='top right')
                    else:
                        # Padronizado para :.1f
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana: {med_l:.1f}</b>",
                                      annotation_position='top right')

                        if med_g is not None:
                            # Padronizado para :.1f
                            fig.add_hline(y=med_g, line_dash='dash', line_color='crimson',
                                          annotation_text=f"<b>Mediana Geral: {med_g:.1f}</b>",
                                          annotation_position='top right')
            except: pass

        fig.update_traces(textposition='inside')
        fig.update_layout(template="plotly_white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          xaxis=dict(title=None, tickangle=-45, automargin=True, categoryorder="array", categoryarray=ordem),
                          yaxis=dict(title=None), margin=dict(l=20, r=20, t=65, b=60))
        largura, altura = ajustar_tamanho_grafico(df_t, altura_min=350)
        graficos.append(html.Div(dcc.Graph(figure=fig, config={'responsive': True}, style={'height': altura, 'width': largura}),
                                 style={'flex': '0 0 auto', 'backgroundColor': 'white', 'borderRadius': '12px', 'padding': '15px', 'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'}))

    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})
def gerar_graficos_registros(dfs, modo, metricas=None, exibir_mediana=False):
    metricas_registros = ["REGISTROS DE SW", "PATENTES"]
    graficos = []
    df_plot_list = []

    for nome, df in dfs.items():
        if modo == 'geral' and nome == 'total':
            df_tmp = df.copy(); df_tmp['X'] = 'Total'; df_plot_list.append(df_tmp)
        elif modo == 'grupo' and nome != 'total':
            df_tmp = df.iloc[[-1]].copy(); df_tmp['X'] = nome; df_plot_list.append(df_tmp)
        elif modo == 'professor' and nome != 'total':
            df_tmp = df.copy(); df_tmp['X'] = df_tmp.get('Nome', df_tmp.columns[0]); df_plot_list.append(df_tmp)

    if not df_plot_list: return [html.Div("Nenhum dado disponível.")]
    df_total = pd.concat(df_plot_list, ignore_index=True)
    if metricas is not None: metricas_registros = [c for c in metricas_registros if c in metricas]

    for col in metricas_registros:
        if col not in df_total.columns: continue
        df_melt = pd.DataFrame({"X": df_total['X'], "Quantidade": df_total[col]}).sort_values("Quantidade", ascending=False)
        
        # No modo professor, renomear o eixo X para P1, P2, P3, etc. DEPOIS de ordenar
        if modo == 'professor':
            mapa_renomeacao = {df_melt['X'].iloc[i]: f'P{i+1}' for i in range(len(df_melt))}
            df_melt['X'] = df_melt['X'].map(mapa_renomeacao)
        
        fig = px.bar(df_melt, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)

        if exibir_mediana:
            try:
                if len(df_melt) > 0 and modo != 'geral':
                    med_l = float(df_melt['Quantidade'].median())
                    med_g = MEDIANAS_GERAIS.get(col, 0) if modo == 'professor' else None
                    if med_g is not None and med_l == med_g:
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana / Mediana Geral: {med_l:.1f}</b>",
                                      annotation_position='top right')
                    else:
                        # Padronizado para :.1f
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana: {med_l:.1f}</b>",
                                      annotation_position='top right')

                        if med_g is not None:
                            # Padronizado para :.1f
                            fig.add_hline(y=med_g, line_dash='dash', line_color='crimson',
                                          annotation_text=f"<b>Mediana Geral: {med_g:.1f}</b>",
                                          annotation_position='top right')
            except: pass

        fig.update_traces(textposition='inside')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          xaxis=dict(title=None, tickangle=-45, automargin=True, categoryorder="array", categoryarray=df_melt["X"]),
                          yaxis=dict(title=None),margin=dict(l=40, r=120, t=65, b=80))
        largura, altura = ajustar_tamanho_grafico(df_total, altura_min=350)
        graficos.append(html.Div(
            dcc.Graph(
                figure=fig,
                config={'responsive': True},
                style={'height': altura, 'width': largura}
            ),
            style={
                'flex': '0 0 auto',
                'backgroundColor': 'white',
                'borderRadius': '12px',
                'padding': '15px',
                'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)',
                'marginRight': '15px',
                'minWidth': largura
            }
        ))
    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})
def gerar_graficos_publicacoes(dfs, modo, metricas=None, exibir_mediana=False):
    metricas_publicacoes = ['PUBLICAÇÕES CIENTÍFICAS', 'LIVROS ISBN', 'CAPÍTULOS ISBN', 'PUB. TRAB. EVENTOS']
    todas_metricas = metricas_publicacoes
    graficos = []

    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty: return []
        if 'Nome' in df_total.columns: df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()
        df_total['X'] = df_total['Nome']
    elif modo == 'geral':
        df_total = dfs.get("total", pd.DataFrame()).copy(); df_total['X'] = "Total"
    elif modo == 'grupo':
        df_plot_list = [df.copy().assign(X=nome) for nome, df in dfs.items() if nome != "total"]
        if not df_plot_list: return [html.Div("Nenhum dado disponível.")]
        df_total = pd.concat(df_plot_list, ignore_index=True)
    else: return [html.Div("Modo inválido.")]

    if metricas is not None: todas_metricas = [c for c in todas_metricas if c in metricas]

    for col in todas_metricas:
        if not any(col in df.columns for df in dfs.values()): continue
        df_plot = df_total.groupby("X", as_index=False)[col].sum().rename(columns={col: "Quantidade"}).sort_values("Quantidade", ascending=False)
        
        # No modo professor, renomear o eixo X para P1, P2, P3, etc. DEPOIS de ordenar
        if modo == 'professor':
            mapa_renomeacao = {df_plot['X'].iloc[i]: f'P{i+1}' for i in range(len(df_plot))}
            df_plot['X'] = df_plot['X'].map(mapa_renomeacao)
        
        fig = px.bar(df_plot, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)

        if exibir_mediana:
            try:
                if len(df_plot) > 0 and modo != 'geral':
                    med_l = float(df_plot['Quantidade'].median())
                    med_g = MEDIANAS_GERAIS.get(col, 0) if modo == 'professor' else None
                    if med_g is not None and med_l == med_g:
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana / Mediana Geral: {med_l:.1f}</b>",
                                      annotation_position='top right')
                    else:
                        # Padronizado para :.1f
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana: {med_l:.1f}</b>",
                                      annotation_position='top right')

                        if med_g is not None:
                            # Padronizado para :.1f
                            fig.add_hline(y=med_g, line_dash='dash', line_color='crimson',
                                          annotation_text=f"<b>Mediana Geral: {med_g:.1f}</b>",
                                          annotation_position='top right')
            except: pass

        fig.update_traces(textposition='inside')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          xaxis=dict(title=None, tickangle=-45, automargin=True, categoryorder="array", categoryarray=df_plot["X"]),
                          yaxis=dict(title=None), margin=dict(l=40, r=120, t=65, b=80))
        largura, altura = ajustar_tamanho_grafico(df_total)
        graficos.append(html.Div(
            dcc.Graph(
                figure=fig,
                config={'responsive': True},
                style={'height': altura, 'width': '100%'}
            ),
            style={
                'flex': '1 1 auto',
                'minWidth': '300px',
                'backgroundColor': 'white',
                'borderRadius': '12px',
                'padding': '15px',
                'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)',
                'marginRight': '15px',
            }
        ))
    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})
def gerar_graficos_outros(dfs, modo, metricas=None, exibir_mediana=False):
    metricas_outros = ['EVENTOS ORGANIZADOS', 'PUB. TEC. E ART.']
    todas_metricas = metricas_outros
    graficos = []

    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty: return []
        if 'Nome' in df_total.columns: df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()
        df_total['X'] = df_total['Nome']
    elif modo == 'geral':
        df_total = dfs.get("total", pd.DataFrame()).copy(); df_total['X'] = "Total"
    elif modo == 'grupo':
        df_plot_list = [df.copy().assign(X=nome) for nome, df in dfs.items() if nome != "total"]
        if not df_plot_list: return [html.Div("Nenhum dado disponível.")]
        df_total = pd.concat(df_plot_list, ignore_index=True)
    else: return [html.Div("Modo inválido.")]

    if metricas is not None: todas_metricas = [c for c in todas_metricas if c in metricas]

    for col in todas_metricas:
        if not any(col in df.columns for df in dfs.values()): continue
        df_plot = df_total.groupby("X", as_index=False)[col].sum().rename(columns={col: "Quantidade"}).sort_values("Quantidade", ascending=False)
        
        # No modo professor, renomear o eixo X para P1, P2, P3, etc. DEPOIS de ordenar
        if modo == 'professor':
            mapa_renomeacao = {df_plot['X'].iloc[i]: f'P{i+1}' for i in range(len(df_plot))}
            df_plot['X'] = df_plot['X'].map(mapa_renomeacao)
        
        fig = px.bar(df_plot, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)

        if exibir_mediana:
            try:
                if len(df_plot) > 0 and modo != 'geral':
                    med_l = float(df_plot['Quantidade'].median())
                    med_g = MEDIANAS_GERAIS.get(col, 0) if modo == 'professor' else None
                    if med_g is not None and med_l == med_g:
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana / Mediana Geral: {med_l:.1f}</b>",
                                      annotation_position='top right')
                    else:
                        # Padronizado para :.1f
                        fig.add_hline(y=med_l, line_dash='dash', line_color='crimson',
                                      annotation_text=f"<b>Mediana: {med_l:.1f}</b>",
                                      annotation_position='top right')

                        if med_g is not None:
                            # Padronizado para :.1f
                            fig.add_hline(y=med_g, line_dash='dash', line_color='crimson',
                                          annotation_text=f"<b>Mediana Geral: {med_g:.1f}</b>",
                                          annotation_position='top right')
            except: pass

        fig.update_traces(textposition='inside')
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                          xaxis=dict(title=None, tickangle=-45, automargin=True, categoryorder="array", categoryarray=df_plot["X"]),
                          yaxis=dict(title=None), margin=dict(l=40, r=120, t=65, b=80))
        largura, altura = ajustar_tamanho_grafico(df_total)
        graficos.append(html.Div(
            dcc.Graph(
                figure=fig,
                config={'responsive': True},
                style={'height': altura, 'width': largura}
            ),
            style={
                'flex': '0 0 auto',  #
                'backgroundColor': 'white',
                'borderRadius': '12px',
                'padding': '15px',
                'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)',
                'marginRight': '15px',
                'minWidth': largura
            }
        ))
    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap', 'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})

@callback(
    Output('store-modo-atual', 'data'),
    Input('btn-geral', 'n_clicks'),
    Input('btn-grupo', 'n_clicks'),
    Input('btn-professor', 'n_clicks'),
)
def guardar_modo_atual(btn_geral, btn_grupo, btn_professor):
    ctx = callback_context
    if not ctx.triggered:
        return 'geral'
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')
    return modo

@callback(
    Output('filtro-status-orientacoes', 'value'),
    Output('filtro-tipo-orientacoes', 'value'),
    Output('filtro-natureza-orientacoes', 'value'),
    Output('filtro-grupo-orientacoes', 'value'),
    Output('filtro-grupo-registros', 'value'),
    Output('filtro-grupo-publicacoes', 'value'),
    Output('filtro-grupo-outros', 'value'),
    Input('store-modo-atual', 'data'),
    prevent_initial_call=True
)
def resetar_filtros_ao_mudar_modo(modo_selecionado):
    return 'ambos', 'todos', 'soma', None, None, None


@callback(
    Output("container-graficos", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),
    Input("filtro-status-orientacoes", "value"),
    Input("filtro-tipo-orientacoes", "value"),
    Input("filtro-natureza-orientacoes", "value"),
    Input("filtro-grupo-orientacoes", "value"),
    Input("check-mediana-orientacoes", "value"),  # NOVO INPUT
    State("store-lista-dfs", "data")
)
def atualizar_graficos_orientacoes(selected_viz, modo_atual, status, tipo, natureza,
                                   grupo_selecionado, check_mediana, stored_data):
    if not stored_data or "orientacoes" not in selected_viz:
        return []

    exibir = 'SIM' in (check_mediana or [])
    modo = modo_atual if modo_atual else 'geral'
    dfs, metricas = parse_stored_data(stored_data)
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)

    return gerar_graficos_orientacoes(dfs_filtrados, status, tipo, natureza, modo, metricas, exibir_mediana=exibir)


@callback(
    Output("container-graficos-registros", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),
    Input("filtro-grupo-registros", "value"),
    Input("check-mediana-registros", "value"),  # NOVO INPUT
    State("store-lista-dfs", "data")
)
def atualizar_graficos_registros(selected_viz, modo_atual, grupo_selecionado, check_mediana, stored_data):
    if not stored_data or "registros" not in selected_viz:
        return []

    exibir = 'SIM' in (check_mediana or [])
    modo = modo_atual if modo_atual else 'geral'
    dfs, metricas = parse_stored_data(stored_data)
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)

    return gerar_graficos_registros(dfs_filtrados, modo, metricas, exibir_mediana=exibir)


@callback(
    Output("container-graficos-publicacoes", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),
    Input("filtro-grupo-publicacoes", "value"),
    Input("check-mediana-publicacoes", "value"),  # NOVO INPUT
    State("store-lista-dfs", "data")
)
def atualizar_graficos_publicacoes(selected_viz, modo_atual, grupo_selecionado, check_mediana, stored_data):
    if not stored_data or "publicacoes" not in selected_viz:
        return []

    exibir = 'SIM' in (check_mediana or [])
    modo = modo_atual if modo_atual else 'geral'
    dfs, metricas = parse_stored_data(stored_data)
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)

    return gerar_graficos_publicacoes(dfs_filtrados, modo, metricas, exibir_mediana=exibir)


@callback(
    Output("container-graficos-outros", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),
    Input("filtro-grupo-outros", "value"),
    Input("check-mediana-outros", "value"),  # NOVO INPUT
    State("store-lista-dfs", "data")
)
def atualizar_graficos_outros(selected_viz, modo_atual, grupo_selecionado, check_mediana, stored_data):
    if not stored_data or "outros" not in selected_viz:
        return []

    exibir = 'SIM' in (check_mediana or [])
    modo = modo_atual if modo_atual else 'geral'
    dfs, metricas = parse_stored_data(stored_data)
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)

    return gerar_graficos_outros(dfs_filtrados, modo, metricas, exibir_mediana=exibir)

@callback(
    Output("filtros-orientacoes-container", "children"),
    Input("checklist-viz", "value")
)
def mostrar_filtros_orientacoes(selected_viz):
    if "orientacoes" not in selected_viz:
        return html.Div()
    filtros_padrao = html.Div([
        html.Div([html.Label("Status:", style={'fontWeight': 'bold'}), dcc.Dropdown(
            id="filtro-status-orientacoes",
            options=[{"label": "Em andamento", "value": "andamento"}, {"label": "Concluído", "value": "concluido"},
                     {"label": "Ambos", "value": "ambos"}], value="ambos", clearable=False
        )], style={"display": "inline-block", "marginRight": "10px", 'width': '150px'}),
        html.Div([html.Label("Tipo:", style={'fontWeight': 'bold'}), dcc.Dropdown(
            id="filtro-tipo-orientacoes",
            options=[{"label": "IC", "value": "ic"}, {"label": "Mestrado", "value": "mestrado"},
                     {"label": "Doutorado", "value": "doutorado"}, {"label": "Todos", "value": "todos"},
                     {"label": "TCC Concluído", "value": "tcc-conc"}, {"label": "Especialização Concluída", "value": "conc-esp"},],
            value="todos",

            clearable=False
        )], style={"display": "inline-block", "marginRight": "10px", 'width': '150px'}),
        html.Div([html.Label("Natureza:", style={'fontWeight': 'bold'}), dcc.Dropdown(
            id="filtro-natureza-orientacoes", options=[{"label": "Orientações", "value": "orientacoes"},
                                                       {"label": "Coorientações", "value": "coorientacoes"},
                                                       {"label": "Soma dos dois", "value": "soma"}], value="soma",
            clearable=False
        )], style={"display": "inline-block", 'width': '150px'}),
    ], style={"display": "flex", "gap": "20px"})
    filtro_condicional = html.Div(
        id='wrapper-filtro-orientacoes', style={'display': 'none'},
        children=[
            html.Div([
                html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id="filtro-grupo-orientacoes", options=[], clearable=True, placeholder="Todos os grupos")
            ], style={'width': '300px', 'marginLeft': '20px'})
        ]
    )
    return html.Div([filtros_padrao, filtro_condicional], style={'display': 'flex', 'alignItems': 'center'})


@callback(
    [Output("check-mediana-orientacoes", "style"),
     Output("check-mediana-registros", "style"),
     Output("check-mediana-publicacoes", "style"),
     Output("check-mediana-outros", "style")],
    Input('store-modo-atual', 'data')
)
def gerenciar_visibilidade_mediana(modo_atual):
    if modo_atual == 'geral':
        estilo = {'display': 'none'}
    else:
        estilo = {'textAlign': 'center', 'marginBottom': '10px', 'fontSize': '14px'}

    return [estilo, estilo, estilo, estilo]

@callback(
    Output("wrapper-filtro-publicacoes", "style"),
    Input("btn-professor", "n_clicks"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks")
)
def mostrar_ocultar_filtro_grupo_publicacoes(btn_professor, btn_geral, btn_grupo):
    ctx = callback_context
    if not ctx.triggered: return {'display': 'none'}
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn_id == 'btn-professor':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output("wrapper-filtro-outros", "style"),
    Input("btn-professor", "n_clicks"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks")
)
def mostrar_ocultar_filtro_grupo_outros(btn_professor, btn_geral, btn_grupo):
    ctx = callback_context
    if not ctx.triggered: return {'display': 'none'}
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn_id == 'btn-professor':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output("wrapper-filtro-orientacoes", "style"),
    Input("btn-professor", "n_clicks"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks")
)
def mostrar_ocultar_filtro_grupo_orientacoes(btn_professor, btn_geral, btn_grupo):
    ctx = callback_context
    if not ctx.triggered: return {'display': 'none'}
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn_id == 'btn-professor':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@callback(
    Output("wrapper-filtro-registros", "style"),
    Input("btn-professor", "n_clicks"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks")
)
def mostrar_ocultar_filtro_grupo_registros(btn_professor, btn_geral, btn_grupo):
    ctx = callback_context
    if not ctx.triggered: return {'display': 'none'}
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn_id == 'btn-professor':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@callback(
    Output("filtro-grupo-publicacoes", "options"),
    Output("filtro-grupo-outros", "options"),
    Output("filtro-grupo-orientacoes", "options"),
    Output("filtro-grupo-registros", "options"),
    Input("store-lista-dfs", "data")
)
def popular_opcoes_de_grupo(stored_data):
    if not stored_data:
        return [], [], [], []
    dfs, metricas = parse_stored_data(stored_data)
    grupos = [{"label": g, "value": g} for g in dfs.keys() if g != "total"]
    # Retorna 4 outputs sempre (ordem: publicacoes, outros, orientacoes, registros)
    return grupos, grupos, grupos, grupos


@callback(
    Output('checklist-viz', 'options'),
    Output('checklist-viz', 'value'),
    Input('store-lista-dfs', 'data'),
    State('checklist-viz', 'value')
)
def atualizar_checklist_viz_por_metricas(stored_data, current_value):
    """Desabilita itens do checklist de visualizações quando não houver métricas correspondentes.
    Também remove valores desabilitados do `value` para manter consistência.
    """
    default_options = [
        {'label': 'Registros', 'value': 'registros'},
        {'label': 'Orientações', 'value': 'orientacoes'},
        {'label': 'Publicações', 'value': 'publicacoes'},
        {'label': 'Outros', 'value': 'outros'},
    ]

    # sem dados armazenados, mantém opções padrão e valor atual
    if not stored_data:
        # se value for None (render inicial), retorna todos selecionados
        if not current_value:
            return default_options, [opt['value'] for opt in default_options]
        return default_options, current_value

    dfs, metricas = parse_stored_data(stored_data)

    # detecta presença por categoria com base nas métricas explícitas
    orientacoes_present = any(m for m in metricas if m.startswith('O.P') or m.startswith('C.O') or m.startswith('ORIENTA'))
    registros_present = any(m in metricas for m in ["PATENTES", "REGISTROS DE SW"]) 
    publicacoes_present = any(m in metricas for m in ['PUBLICAÇÕES CIENTÍFICAS', 'LIVROS ISBN', 'CAPÍTULOS ISBN', 'PUB. TRAB. EVENTOS'])
    outros_present = any(m in metricas for m in ['EVENTOS ORGANIZADOS', 'PUB. TEC. E ART.'])

    options_all = [
        {'label': 'Registros', 'value': 'registros'},
        {'label': 'Orientações', 'value': 'orientacoes'},
        {'label': 'Publicações', 'value': 'publicacoes'},
        {'label': 'Outros', 'value': 'outros'},
    ]

    # filtra apenas as opções que têm métricas correspondentes (oculta as demais)
    options = []
    if registros_present:
        options.append(options_all[0])
    if orientacoes_present:
        options.append(options_all[1])
    if publicacoes_present:
        options.append(options_all[2])
    if outros_present:
        options.append(options_all[3])

    # ajusta value removendo itens que foram ocultados
    if not current_value:
        new_value = [opt['value'] for opt in options]
    else:
        new_value = [v for v in current_value if any(o['value'] == v for o in options)]

    return options, new_value


@callback(
    Output('btn-geral', 'style'),
    Output('btn-grupo', 'style'),
    Output('btn-professor', 'style'),
    Input('btn-geral', 'n_clicks'),
    Input('btn-grupo', 'n_clicks'),
    Input('btn-professor', 'n_clicks'),
)
def atualizar_modo(btn_geral, btn_grupo, btn_professor):
    ctx = callback_context
    if not ctx.triggered:
        modo = 'geral'
    else:
        btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
        modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')

    def style_botao(ativo):
        base = {'padding': '10px 10px', 'border': 'none', 'borderRadius': '20px', 'margin': '5px', 'cursor': 'pointer',
                'boxShadow': '0px 2px 5px rgba(0,0,0,0.2)'}
        base['backgroundColor'] = '#28a745' if ativo else '#ccc'
        base['color'] = 'white' if ativo else '#666'
        return base

    return style_botao(modo == 'geral'), style_botao(modo == 'grupo'), style_botao(modo == 'professor')


@callback(
    Output("section-orientacoes", "style"),
    Output("section-registros", "style"),
    Output("section-publicacoes", "style"),
    Output("section-outros", "style"),
    Input("checklist-viz", "value"),
    Input("store-lista-dfs", "data")
)
def toggle_sections(selected_viz, stored_data):

    # comportamento padrão baseado apenas no checklist (quando não há dados armazenados)
    default_style = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
                     "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%", "maxWidth": "1400px"}
    hidden = {"display": "none"}

    # se não há dados armazenados, usa apenas o checklist
    if not stored_data:
        style_orientacoes = default_style if "orientacoes" in selected_viz else hidden
        style_registros = default_style if "registros" in selected_viz else hidden
        style_publicacoes = default_style if "publicacoes" in selected_viz else hidden
        style_outros = default_style if "outros" in selected_viz else hidden
        return style_orientacoes, style_registros, style_publicacoes, style_outros

    # usa as métricas explícitas gravadas em _meta (mais confiável que inspecionar colunas)
    dfs, metricas = parse_stored_data(stored_data)

    orientacoes_present = any(m for m in metricas if m.startswith('O.P') or m.startswith('C.O') or m.startswith('ORIENTA'))
    registros_present = any(m in metricas for m in ["PATENTES", "REGISTROS DE SW"])
    publicacoes_present = any(m in metricas for m in ['PUBLICAÇÕES CIENTÍFICAS', 'LIVROS ISBN', 'CAPÍTULOS ISBN', 'PUB. TRAB. EVENTOS'])
    outros_present = any(m in metricas for m in ['EVENTOS ORGANIZADOS', 'PUB. TEC. E ART.'])

    style_orientacoes = default_style if ("orientacoes" in selected_viz and orientacoes_present) else hidden
    style_registros = default_style if ("registros" in selected_viz and registros_present) else hidden
    style_publicacoes = default_style if ("publicacoes" in selected_viz and publicacoes_present) else hidden
    style_outros = default_style if ("outros" in selected_viz and outros_present) else hidden

    return style_orientacoes, style_registros, style_publicacoes, style_outros

def generate_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        wrote_any = False
        for sheet_name, json_data in data.items():
            df = pd.read_json(io.StringIO(json_data), orient='split')
            # só escreve abas que contenham métricas além de 'Nome' e 'ID LATTES'
            metric_cols = [c for c in df.columns if c not in ['Nome', 'ID LATTES']]
            if metric_cols:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                wrote_any = True

        if not wrote_any:
            # cria uma aba resumo indicando que não há métricas selecionadas
            resumo = pd.DataFrame({"Info": ["Nenhuma métrica selecionada ou dados disponíveis para exportar."]})
            resumo.to_excel(writer, sheet_name='Resumo', index=False)
    output.seek(0)
    return output

@callback(
    Output("download-dataframe-xlsx", "data"),
    Input("btn-download", "n_clicks"),
    State("store-lista-dfs", "data"),
    prevent_initial_call=True
)
def download_excel(n_clicks, stored_data):
    if not stored_data:
        raise PreventUpdate
    dfs, metricas = parse_stored_data(stored_data)
    excel_io = generate_excel({k: df.to_json(orient='split') for k, df in dfs.items()})
    return dcc.send_bytes(excel_io.getvalue(), "dados_extrator_lattes.xlsx")

mapa_professores = {}


def anonimizar_nomes(df, coluna_nome='Nome'):
    mapa_local = {}

    if coluna_nome not in df.columns:
        return df.copy()

    df_anon = df.copy()

    for nome in df[coluna_nome].dropna().unique():
        if nome not in mapa_local:
            mapa_local[nome] = f"P{len(mapa_local) + 1}"

    df_anon[coluna_nome] = df[coluna_nome].map(mapa_local)
    return df_anon

def filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado=None):
    if modo == 'geral':
        df_total = dfs.get('total', pd.DataFrame())
        if not df_total.empty:
            return {'total': df_total.iloc[[-1]]}
        return {'total': pd.DataFrame()}

    elif modo == 'grupo':
        dfs_grupos = {}
        for k, df in dfs.items():
            if k != 'total':
                dfs_grupos[k] = df.iloc[[-1]]
        return dfs_grupos

    elif modo == 'professor':
        # se um grupo foi selecionado usa só esse grupo # nao esta funcionando
        lista_dfs_professores = []
        grupos_para_usar = [grupo_selecionado] if grupo_selecionado and grupo_selecionado in dfs else [k for k in dfs if k != "total"]

        for k in grupos_para_usar:
            df = dfs[k]
            df_filtrado = df.iloc[:-1].copy()  # remove linha de total
            df_filtrado['Grupo/Programa'] = k
            lista_dfs_professores.append(df_filtrado)

        if lista_dfs_professores:
            df_final = pd.concat(lista_dfs_professores, ignore_index=True)
            return {'professores': df_final}
        return {'professores': pd.DataFrame()}

    return dfs


def parse_stored_data(stored_data):
    """Retorna um dict de DataFrames e a lista de métricas selecionadas (meta) do stored_data.
    stored_data pode ter valores JSON (string) ou já dicts; também pode conter a chave '_meta'.
    """
    dfs = {}
    metricas = []
    if not stored_data:
        return dfs, metricas

    for k, v in stored_data.items():
        if k == '_meta':
            # meta pode ser um dict ou string JSON
            if isinstance(v, dict):
                metricas = v.get('metricas', [])
            else:
                try:
                    meta = json.loads(v)
                    metricas = meta.get('metricas', [])
                except Exception:
                    metricas = []
            continue

        try:
            if isinstance(v, str):
                df = pd.read_json(io.StringIO(v), orient='split')
            elif isinstance(v, dict):
                # caso o valor já seja uma estrutura serializada (fallback)
                df = pd.DataFrame(v)
            else:
                # tentativa de carregar diretamente
                df = pd.read_json(io.StringIO(str(v)), orient='split')
            dfs[k] = df
        except Exception:
            # ignora entradas que não são DataFrames
            continue

    # Normaliza metricas: mantém apenas métricas que existem nas colunas dos DataFrames
    if dfs:
        available_metrics = set()
        for df in dfs.values():
            available_metrics.update([c for c in df.columns if isinstance(c, str)])
        metricas = [m for m in metricas if m in available_metrics]

    return dfs, metricas