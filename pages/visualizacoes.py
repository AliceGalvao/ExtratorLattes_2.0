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
                    {'label': 'Eventos e Publicações', 'value': 'eventos_publicacoes'}
                ],
                value=['registros', 'orientacoes', 'eventos_publicacoes'],
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
        html.Div(id="filtros-registros-container"),
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

    html.Div(id="section-eventos", children=[
        html.H3("Eventos e Publicações", style={'textAlign': 'center', 'marginBottom': '15px'}),
        html.Div(id="filtros-eventos-container"),
        html.Div(id="container-graficos-eventos", style={
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

    dcc.Download(id="download-dataframe-xlsx")
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
        "ic": {"orientacoes": {"concluido": ["ORIENTAÇÕES I.C"], "andamento": []}, "coorientacoes": {"concluido": [], "andamento": []}}
    }

    tipos_a_mostrar = list(colunas_map.keys()) if tipo == "todos" else [tipo]
    dados_plot = []

    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty:
            return [html.Div("Nenhum dado disponível.")]
        if 'Nome' in df_total.columns:
            df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]

        todas_metricas = [
            "O.P MESTRADO CONC.", "O.P MESTRADO AND.",
            "C.O MESTRADO CONC.", "C.O MESTRADO AND.",
            "O.P DOUTORADO CONC.", "O.P DOUTORADO AND.",
            "C.O DOUTORADO CONC.", "C.O DOUTORADO AND.",
            "ORIENTAÇÕES I.C"
        ]
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()

        for index, row in df_total.iterrows():
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
            fig = px.bar(title=f"{t.upper()} - Sem dados")
            fig.update_layout(yaxis={"visible": False}, xaxis={"visible": False})
        else:
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
                xaxis=dict(title=None, tickangle=-45, automargin=True),
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
            fig = px.bar(df_melt, x="X", y="Quantidade", title=col, template="plotly_white", text_auto=True)
            fig.update_traces(textposition='inside')
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=None, tickangle=-45, automargin=True),
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

def gerar_graficos_eventos_publicacoes(dfs, modo, grupo_selecionado=None):
    metricas_eventos = ['EVENTOS ORGANIZADOS', 'PUB. TRAB. EVENTOS']
    metricas_publicacoes = ['PUBLICAÇÕES CIENTÍFICAS', 'LIVROS ISBN', 'CAPÍTULOS ISBN', 'PUB. TEC. E ART.']
    todas_metricas = metricas_eventos + metricas_publicacoes
    graficos = []

    #  usa so o df de professores
    if modo == 'professor':
        df_total = dfs.get("professores", pd.DataFrame()).copy()
        if df_total.empty:
            return [html.Div("Nenhum dado disponível.")]

        # remove possiveis linhas de totais
        if 'Nome' in df_total.columns:
            df_total = df_total[~df_total['Nome'].astype(str).str.upper().str.contains('TOTAL')]

        # agrega pra garantir que um professor não apareça duplicado
        cols_to_agg = [c for c in todas_metricas if c in df_total.columns]
        df_total = df_total.groupby('Nome', as_index=False)[cols_to_agg].sum()
        df_total['X'] = df_total['Nome']

    # mostra apenas o total geral
    elif modo == 'geral':
        df_total = dfs.get("total", pd.DataFrame()).copy()
        if df_total.empty:
            return [html.Div("Nenhum dado disponível.")]
        df_total['X'] = "Total"

    # mostra o total por grupo
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

            fig = px.bar(df_plot, x="X", y="Quantidade", title=col,
                         template="plotly_white", text_auto=True)
            fig.update_traces(textposition='inside')
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(title=None, tickangle=-45, automargin=True),
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
    Output("container-graficos", "children"),
    Input("checklist-viz", "value"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks"),
    Input("btn-professor", "n_clicks"),
    Input("filtro-status-orientacoes", "value"),
    Input("filtro-tipo-orientacoes", "value"),
    Input("filtro-natureza-orientacoes", "value"),
    State("store-lista-dfs", "data")
)
def atualizar_graficos_orientacoes(selected_viz, btn_geral, btn_grupo, btn_professor,
                                   status, tipo, natureza, stored_data):
    if not stored_data or "orientacoes" not in selected_viz:
        return []
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    ctx = callback_context
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-geral'
    modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo)
    return gerar_graficos_orientacoes(dfs_filtrados, status, tipo, natureza, modo) # Passando 'modo'

@callback(
    Output("container-graficos-registros", "children"),
    Input("checklist-viz", "value"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks"),
    Input("btn-professor", "n_clicks"),
    State("store-lista-dfs", "data")
)
def atualizar_graficos_registros(selected_viz, btn_geral, btn_grupo, btn_professor, stored_data):
    if not stored_data or "registros" not in selected_viz:
        return []

    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    ctx = callback_context
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-geral'
    modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')

    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo)

    return gerar_graficos_registros(dfs_filtrados, modo)

@callback(
    Output("container-graficos-eventos", "children"),
    Input("checklist-viz", "value"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks"),
    Input("btn-professor", "n_clicks"),
    State("store-lista-dfs", "data")
)
def atualizar_graficos_eventos(selected_viz, btn_geral, btn_grupo, btn_professor, stored_data):
    if not stored_data or "eventos_publicacoes" not in selected_viz:
        return []
    dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
    ctx = callback_context
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-geral'
    modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')
    dfs_filtrados = filtrar_dfs_para_graficos(dfs, modo)
    return gerar_graficos_eventos_publicacoes(dfs_filtrados, modo)

@callback(
    Output("filtros-orientacoes-container", "children"),
    Input("checklist-viz", "value")
)
def mostrar_filtros_orientacoes(selected_viz):
    if "orientacoes" not in selected_viz:
        return html.Div()

    return html.Div([
        html.Div([html.Label("Status:"), dcc.Dropdown(
            id="filtro-status-orientacoes",
            options=[{"label": "Em andamento", "value": "andamento"},
                     {"label": "Concluído", "value": "concluido"},
                     {"label": "Ambos", "value": "ambos"}],
            value="ambos",
            clearable=False
        )], style={"display":"inline-block", "marginRight":"10px", 'width':'150px'}),
        html.Div([html.Label("Tipo:"), dcc.Dropdown(
            id="filtro-tipo-orientacoes",
            options=[{"label": "IC", "value": "ic"},
                     {"label": "Mestrado", "value": "mestrado"},
                     {"label": "Doutorado", "value": "doutorado"},
                     {"label": "Todos", "value": "todos"}],
            value="todos",
            clearable=False
        )], style={"display":"inline-block", "marginRight":"10px", 'width':'150px'}),
        html.Div([html.Label("Natureza:"), dcc.Dropdown(
            id="filtro-natureza-orientacoes",
            options=[{"label": "Orientações", "value": "orientacoes"},
                     {"label": "Coorientações", "value": "coorientacoes"},
                     {"label": "Soma dos dois", "value": "soma"}],
            value="soma",
            clearable=False
        )], style={"display":"inline-block", 'width':'150px'}),
    ], style={"display":"flex", "gap":"20px"})

@callback(
    Output("filtros-eventos-container", "children"),
    Input("checklist-viz", "value"),
    Input("btn-geral", "n_clicks"),
    Input("btn-grupo", "n_clicks"),
    Input("btn-professor", "n_clicks"),
    State("store-lista-dfs", "data")
)
def mostrar_filtros_eventos(selected_viz, btn_geral, btn_grupo, btn_professor, stored_data):
    if "eventos_publicacoes" not in selected_viz:
        return html.Div()

    ctx = callback_context
    btn_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'btn-geral'
    modo = {'btn-geral': 'geral', 'btn-grupo': 'grupo', 'btn-professor': 'professor'}.get(btn_id, 'geral')

    if modo != 'professor':
        return html.Div()

    grupos_disponiveis = []
    if stored_data:
        dfs = {k: pd.read_json(io.StringIO(v), orient='split') for k, v in stored_data.items()}
        grupos_disponiveis = [k for k in dfs.keys() if k != "total"]

    return html.Div([
        html.Div([
            html.Label("Selecione o grupo:"),
            dcc.Dropdown(
                id="filtro-grupo-eventos",
                options=[{"label": g, "value": g} for g in grupos_disponiveis],
                value=grupos_disponiveis[0] if grupos_disponiveis else None,
                clearable=False,
            )
        ], style={"display": "inline-block", "marginRight": "10px", "width": "200px"}),
    ])

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
        modo = {'btn-geral':'geral','btn-grupo':'grupo','btn-professor':'professor'}.get(btn_id,'geral')

    def style_botao(ativo):
        base = {'padding': '10px 10px', 'border': 'none', 'borderRadius': '20px', 'margin': '5px',
                'cursor': 'pointer', 'boxShadow': '0px 2px 5px rgba(0,0,0,0.2)'}
        base['backgroundColor'] = '#28a745' if ativo else '#ccc'
        base['color'] = 'white' if ativo else '#666'
        return base

    return style_botao(modo == 'geral'), style_botao(modo == 'grupo'), style_botao(modo == 'professor')


@callback(
    Output("section-orientacoes", "style"),
    Output("section-registros", "style"),
    Output("section-eventos", "style"),
    Input("checklist-viz", "value")
)
def toggle_sections(selected_viz):
    style_orientacoes = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9",
                         "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
                         "width": "95%", "maxWidth": "1400px"} if "orientacoes" in selected_viz else {"display": "none"}

    style_registros = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9",
                       "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
                       "width": "95%", "maxWidth": "1400px"} if "registros" in selected_viz else {"display": "none"}

    style_eventos = {"margin": "20px auto", "padding": "20px", "backgroundColor": "#f9f9f9",
                     "borderRadius": "10px", "boxShadow": "0 3px 8px rgba(0,0,0,0.1)",
                     "width": "95%", "maxWidth": "1400px"} if "eventos_publicacoes" in selected_viz else {"display": "none"}

    return style_orientacoes, style_registros, style_eventos

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

def generate_excel(data):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, json_data in data.items():
            df = pd.read_json(io.StringIO(json_data), orient='split')
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output

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