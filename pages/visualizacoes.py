import io
import dash
from dash import html, dcc, Input, Output, State, callback, callback_context
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/visualizacoes', name="Visualizações")

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
            ], style={'display': 'flex', 'flexWrap': 'wrap'})
        ], style={'width': '45%', 'padding': '10px'}),

        html.Div([
            html.Div("Escolha as visualizações que deseja exibir:", style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Checklist(
                id='checklist-viz',
                options=[
                    {'label': 'Registros', 'value': 'registros'},
                    {'label': 'Orientações', 'value': 'orientacoes'},
                    {'label': 'Publicações', 'value': 'publicacoes'},
                    {'label': 'Outros', 'value': 'outros'}
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
        ], style={'width': '20%', 'padding': '10px', 'textAlign': 'right', 'display': 'flex', 'alignItems': 'center'})
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
        html.Div(id="filtros-orientacoes-container"),
        html.Div(id="container-graficos", style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'nowrap',
            'overflowX': 'auto',
            'padding': '10px',
            'gap': '15px',
            'width': '100%',
            'height': '450px'
        })
    ], style={"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9",
              "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
              "width": "95%", "maxWidth": "1500px"}),

    html.Div(id="section-registros", children=[
        html.H3("Registros", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div(id="filtros-registros-container",
                 children=[html.Div(id="wrapper-filtro-registros",
                                    style={'display': 'none'},
                                    children=[
                                        html.Div([
                                        html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom':'5px'}),
                                        dcc.Dropdown(id="filtro-grupo-registros", options=[], clearable=True, placeholder="Selecione o grupo")
                                        ], style={'width':'300px','display': 'flex', 'flexDirection': 'column', 'margin-left':'20px'})
                                    ])
            ]),
        html.Div(id="container-graficos-registros", style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'nowrap',
            'overflowX': 'auto',
            'padding': '10px',
            'gap': '15px',
            'width': '100%',
            'height': '450px'
        })
    ], style={"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9",
              "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
              "width": "95%", "maxWidth": "1500px"}),

    html.Div(id="section-publicacoes", children=[
        html.H3("Publicações", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div(id="filtros-publicacoes-container",
                 children =[
                    html.Div(id="wrapper-filtro-publicacoes",
                            style = {'display': 'none'},
                            children=[
                                html.Div([
                                html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom':'5px'}),
                                dcc.Dropdown(id="filtro-grupo-publicacoes", options=[], clearable=True, placeholder="Selecione o grupo")
                                ], style={'width':'300px','display': 'flex', 'flexDirection': 'column', 'margin-left':'20px'} )
                            ])
                     ]),
        html.Div(id="container-graficos-publicacoes", style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'nowrap',
            'overflowX': 'auto',
            'padding': '10px',
            'gap': '15px',
            'width': '100%',
            'height': '450px'
        })
    ], style={"margin": "10px auto", "padding": "10px", "backgroundColor": "#f9f9f9",
              "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
              "width": "95%", "maxWidth": "1500px"}),

    html.Div(id="section-outros", children=[
        html.H3("Outros", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div(id="filtros-outros-container",
                 children =[
                    html.Div(id="wrapper-filtro-outros",
                            style = {'display': 'none'},
                            children=[
                                html.Div([
                                html.Label("Filtrar por Grupo:", style={'fontWeight': 'bold', 'marginBottom':'5px'}),
                                dcc.Dropdown(id="filtro-grupo-outros", options=[], clearable=True, placeholder="Selecione o grupo")
                                ], style={'width':'300px','display': 'flex', 'flexDirection': 'column', 'margin-left':'20px'} )
                            ])
                     ]),
        html.Div(id="container-graficos-outros", style={
            'display': 'flex',
            'flexDirection': 'row',
            'flexWrap': 'nowrap',
            'overflowX': 'auto',
            'padding': '10px',
            'gap': '15px',
            'width': '100%',
            'height': '450px'
        })
    ], style={"margin": "10px auto", "padding": "10px", "backgroundColor": "#f9f9f9",
              "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
              "width": "95%", "maxWidth": "1500px"}),

    dcc.Download(id="download-dataframe-xlsx"),
    dcc.Store(id='store-modo-atual')
])

def ajustar_tamanho_grafico(df, min_barras=6, largura_por_barra=65, altura_por_barra=50,
                            largura_max=1000, altura_max=500, altura_min=350):
    n_barras = max(len(df), min_barras)
    largura = min(n_barras * largura_por_barra, largura_max)
    altura = max(min(n_barras * altura_por_barra, altura_max), altura_min)
    return f"{largura}px", f"{altura}px"

def gerar_graficos_orientacoes(dfs, status, tipo, natureza, modo):
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
        if df_total.empty:
            return []
        if 'Nome' in df_total.columns:
            df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]

        todas_metricas = [
            "O.P MESTRADO CONC.", "O.P MESTRADO AND.",
            "C.O MESTRADO CONC.", "C.O MESTRADO AND.",
            "O.P DOUTORADO CONC.", "O.P DOUTORADO AND.",
            "C.O DOUTORADO CONC.", "C.O DOUTORADO AND.",
            "ORIENTAÇÕES I.C", "ORIENTACOES CONC. ESPECIALIZACAO",
            "ORIENTAÇÕES CONC. TCC"
        ]
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

                if status in ("concluido", "ambos"):
                    dados_plot.append({"Identificador": grupo, "Tipo": t, "Status": "Concluído", "Valor": val_conc})
                if status in ("andamento", "ambos"):
                    dados_plot.append({"Identificador": grupo, "Tipo": t, "Status": "Em andamento", "Valor": val_and})

    df_plot = pd.DataFrame(dados_plot)
    graficos = []

    for t in tipos_a_mostrar:
        df_t = df_plot[df_plot["Tipo"] == t]
        if df_t.empty:
            continue

        ordem = (
            df_t.groupby("Identificador")["Valor"]
            .sum()
            .sort_values(ascending=False)
            .index
            .tolist()
        )

        fig = px.bar(
            df_t,
            x="Identificador",
            y="Valor",
            color="Status",
            barmode="stack",
            title=t.upper(),
            text_auto=True
        )
        fig.update_traces(textposition='inside')
        fig.update_layout(
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(title=None, tickangle=-45, automargin=True,
                       categoryorder="array", categoryarray=ordem),
            yaxis=dict(title=None),
            margin=dict(l=20, r=20, t=65, b=60)
        )

        largura, altura = ajustar_tamanho_grafico(df_t, altura_min=350)
        graficos.append(
            html.Div(
                dcc.Graph(figure=fig, config={'responsive': True}, style={'height': altura, 'width': largura}),
                style={'flex': '0 0 auto',
                       'backgroundColor': 'white',
                       'borderRadius': '12px',
                       'padding': '15px',
                       'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'}
            )
        )

    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap',
                                     'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})


def gerar_graficos_registros(dfs, modo):
    metricas_registros = ["REGISTROS DE SW", "PATENTES"]
    graficos = []
    df_plot_list = []

    for nome, df in dfs.items():
        if modo == 'geral' and nome == 'total':
            df_tmp = df.copy()
            df_tmp['X'] = 'Total'
            df_plot_list.append(df_tmp)
        elif modo == 'grupo' and nome != 'total':
            df_tmp = df.iloc[[-1]].copy()
            df_tmp['X'] = nome
            df_plot_list.append(df_tmp)
        elif modo == 'professor' and nome != 'total':
            df_tmp = df.copy()
            df_tmp['X'] = df_tmp.get('Nome', df_tmp.columns[0])
            df_plot_list.append(df_tmp)

    if not df_plot_list:
        return [html.Div("Nenhum dado disponível.")]

    df_total = pd.concat(df_plot_list, ignore_index=True)

    for col in metricas_registros:
        if col in df_total.columns:
            df_melt = pd.DataFrame({"X": df_total['X'], "Quantidade": df_total[col]})
            df_melt = df_melt.sort_values("Quantidade", ascending=False)

            fig = px.bar(df_melt, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)
            fig.update_traces(textposition='inside')
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=None, tickangle=-45, automargin=True,
                           categoryorder="array", categoryarray=df_melt["X"]),
                yaxis=dict(title=None),
                margin=dict(l=20, r=20, t=40, b=60)
            )
        else:
            fig = px.bar(title=f"{col} - Sem dados")
            fig.update_layout(yaxis={"visible": False}, xaxis={"visible": False})

        largura, altura = ajustar_tamanho_grafico(df_total, altura_min=350)
        graficos.append(
            html.Div(
                dcc.Graph(figure=fig, config={'responsive': True}, style={'height': altura, 'width': largura}),
                style={'flex': '0 0 auto',
                       'backgroundColor': 'white',
                       'borderRadius': '12px',
                       'padding': '15px',
                       'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'}
            )
        )

    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap',
                                     'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})


def gerar_graficos_publicacoes(dfs, modo, grupo_selecionado=None):
    metricas_publicacoes = ['PUBLICAÇÕES CIENTÍFICAS', 'LIVROS ISBN', 'CAPÍTULOS ISBN', 'PUB. TRAB. EVENTOS']
    graficos = []
    df_plot_list = []

    for nome, df in dfs.items():
        if modo == 'geral' and nome == 'total':
            df_tmp = df.copy()
            df_tmp['X'] = 'Total'
            df_plot_list.append(df_tmp)
        elif modo == 'grupo' and nome != 'total':
            df_tmp = df.iloc[[-1]].copy()
            df_tmp['X'] = nome
            df_plot_list.append(df_tmp)
        elif modo == 'professor' and nome != 'total':
            df_tmp = df.copy()
            df_tmp['X'] = df_tmp.get('Nome', df_tmp.columns[0])
            df_plot_list.append(df_tmp)

    if not df_plot_list:
        return [html.Div("Nenhum dado disponível.")]

    df_total = pd.concat(df_plot_list, ignore_index=True)

    for col in metricas_publicacoes:
        if col in df_total.columns:
            df_melt = pd.DataFrame({"X": df_total['X'], "Quantidade": df_total[col]})
            df_melt = df_melt.sort_values("Quantidade", ascending=False)

            fig = px.bar(df_melt, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)
            fig.update_traces(textposition='inside')
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=None, tickangle=-45, automargin=True,
                           categoryorder="array", categoryarray=df_melt["X"]),
                yaxis=dict(title=None),
                margin=dict(l=20, r=20, t=40, b=60)
            )
        else:
            fig = px.bar(title=f"{col} - Sem dados")
            fig.update_layout(yaxis={"visible": False}, xaxis={"visible": False})

        largura, altura = ajustar_tamanho_grafico(df_total, altura_min=350)
        graficos.append(
            html.Div(
                dcc.Graph(figure=fig, config={'responsive': True}, style={'height': altura, 'width': largura}),
                style={'flex': '0 0 auto',
                       'backgroundColor': 'white',
                       'borderRadius': '12px',
                       'padding': '15px',
                       'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'}
            )
        )

    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap',
                                     'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})


def gerar_graficos_outros(dfs, modo, grupo_selecionado=None):
    metricas_outros = ['EVENTOS ORGANIZADOS', 'PUB. TEC. E ART.']
    todas_metricas = metricas_outros
    graficos = []

    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty:
            return []
        if 'Nome' in df_total.columns:
            df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()
        df_total['X'] = df_total['Nome']
    elif modo == 'geral':
        df_total = dfs.get("total", pd.DataFrame()).copy()
        if df_total.empty:
            return []
        df_total['X'] = "Total"
    elif modo == 'grupo':
        df_plot_list = []
        for nome, df in dfs.items():
            if nome != "total":
                df_tmp = df.copy()
                df_tmp['X'] = nome
                df_plot_list.append(df_tmp)
        if not df_plot_list:
            return [html.Div("Nenhum dado disponível.")]
        df_total = pd.concat(df_plot_list, ignore_index=True)
    else:
        return [html.Div("Modo inválido.")]

    for col in todas_metricas:
        if col in df_total.columns:
            df_plot = df_total[["X", col]].copy()
            df_plot = df_plot.groupby("X", as_index=False)[col].sum()
            df_plot.rename(columns={col: "Quantidade"}, inplace=True)
            df_plot = df_plot.sort_values("Quantidade", ascending=False)

            fig = px.bar(df_plot, x="X", y="Quantidade", title=col,
                         template="plotly_white", text_auto=True)
            fig.update_traces(textposition='inside')
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=None, tickangle=-45, automargin=True,
                           categoryorder="array", categoryarray=df_plot["X"]),
                yaxis=dict(title=None),
                margin=dict(l=20, r=20, t=40, b=60)
            )
        else:
            fig = px.bar(title=f"{col} - Sem dados")
            fig.update_layout(yaxis={"visible": False}, xaxis={"visible": False})

        largura, altura = ajustar_tamanho_grafico(df_total)
        graficos.append(
            html.Div(
                dcc.Graph(figure=fig, config={'responsive': True}, style={'height': altura, 'width': largura}),
                style={'flex': '0 0 auto',
                       'backgroundColor': 'white',
                       'borderRadius': '12px',
                       'padding': '15px',
                       'boxShadow': '0px 2px 8px rgba(0,0,0,0.1)'}
            )
        )

    return html.Div(graficos, style={'display': 'flex', 'flexDirection': 'row', 'flexWrap': 'nowrap',
                                     'overflowX': 'auto', 'gap': '15px', 'padding': '10px', 'height': '100%'})



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
    Input('store-modo-atual', 'data'),  # Gatilho: A mudança na memória
    prevent_initial_call=True
)
def resetar_filtros_ao_mudar_modo(modo_selecionado):
    return 'ambos', 'todos', 'soma', None, None, None

@callback(
    Output("container-graficos", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),  # Gatilho principal
    Input("filtro-status-orientacoes", "value"),  # Gatilhos secundários
    Input("filtro-tipo-orientacoes", "value"),
    Input("filtro-natureza-orientacoes", "value"),
    Input("filtro-grupo-orientacoes", "value"),
    State("store-lista-dfs", "data")
)
def atualizar_graficos_orientacoes(selected_viz, modo_atual,
                                   status, tipo, natureza, grupo_selecionado, stored_data):
    if not stored_data or "orientacoes" not in selected_viz:
        return []

    modo = modo_atual if modo_atual else 'geral'
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)
    return gerar_graficos_orientacoes(dfs_filtrados, status, tipo, natureza, modo)


@callback(
    Output("container-graficos-registros", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),  # Gatilho principal
    Input("filtro-grupo-registros", "value"),  # Gatilho secundário
    State("store-lista-dfs", "data")
)
def atualizar_graficos_registros(selected_viz, modo_atual, grupo_selecionado, stored_data):
    if not stored_data or "registros" not in selected_viz:
        return []
    modo = modo_atual if modo_atual else 'geral'
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)
    return gerar_graficos_registros(dfs_filtrados, modo)


@callback(
    Output("container-graficos-publicacoes", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),  # Gatilho principal
    Input("filtro-grupo-publicacoes", "value"),  # Gatilho secundário
    State("store-lista-dfs", "data")
)
def atualizar_graficos_publicacoes(selected_viz, modo_atual, grupo_selecionado, stored_data):
    if not stored_data or "publicacoes" not in selected_viz:
        return []
    modo = modo_atual if modo_atual else 'geral'
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)
    return gerar_graficos_publicacoes(dfs_filtrados, modo)

@callback(
    Output("container-graficos-outros", "children"),
    Input("checklist-viz", "value"),
    Input('store-modo-atual', 'data'),  # Gatilho principal
    Input("filtro-grupo-outros", "value"),  # Gatilho secundário
    State("store-lista-dfs", "data")
)
def atualizar_graficos_outros(selected_viz, modo_atual, grupo_selecionado, stored_data):
    if not stored_data or "outros" not in selected_viz:
        return []
    modo = modo_atual if modo_atual else 'geral'
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo, grupo_selecionado)
    return gerar_graficos_outros(dfs_filtrados, modo)

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
    Output("filtro-grupo-orientacoes", "options"),
    Output("filtro-grupo-registros", "options"),
    Output("filtro-grupo-outros", "options"),
    Input("store-lista-dfs", "data")
)
def popular_opcoes_de_grupo(stored_data):
    if not stored_data:
        return [], [], []
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    grupos = [{"label": g, "value": g} for g in dfs.keys() if g != "total"]
    return grupos, grupos, grupos


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
    Input("checklist-viz", "value")
)
def toggle_sections(selected_viz):
    style_orientacoes = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
                         "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%",
                         "maxWidth": "1400px"} if "orientacoes" in selected_viz else {"display": "none"}
    style_registros = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
                       "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%",
                       "maxWidth": "1400px"} if "registros" in selected_viz else {"display": "none"}
    style_publicacoes = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
                     "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%",
                     "maxWidth": "1400px"} if "publicacoes" in selected_viz else {"display": "none"},
    style_outros = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9", "borderRadius": "10px",
                     "boxShadow": "0 3px 8px rgba(0,0,0,0.1)", "width": "95%",
                     "maxWidth": "1400px"} if "outros" in selected_viz else {"display": "none"}
    return style_orientacoes, style_registros, style_publicacoes, style_outros

def generate_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, json_data in data.items():
            df = pd.read_json(io.StringIO(json_data), orient='split')
            df.to_excel(writer, sheet_name=sheet_name, index=False)
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
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    excel_io = generate_excel({k: df.to_json(orient='split') for k, df in dfs.items()})
    return dcc.send_bytes(excel_io.getvalue(), "dados_extrator_lattes.xlsx")

mapa_professores = {}

def anonimizar_nomes(df, coluna_nome='Nome'):
    global mapa_professores
    if coluna_nome not in df.columns:
        return df.copy()
    df_anon = df.copy()
    for nome in df[coluna_nome].dropna().unique():
        if nome not in mapa_professores:
            mapa_professores[nome] = f"p{len(mapa_professores) + 1}"
    df_anon[coluna_nome] = df[coluna_nome].map(mapa_professores)
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
            df_filtrado = anonimizar_nomes(df_filtrado)
            df_filtrado['Grupo/Programa'] = k
            lista_dfs_professores.append(df_filtrado)

        if lista_dfs_professores:
            df_final = pd.concat(lista_dfs_professores, ignore_index=True)
            return {'professores': df_final}
        return {'professores': pd.DataFrame()}

    return dfs
