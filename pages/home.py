import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import base64
from io import BytesIO
import pandas as pd
import logging

logger = logging.getLogger('dash_app')

dash.register_page(__name__, path='/', name='Início')

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Span("Extrator", style={'color': 'red', 'fontWeight': 'bold'}),
                html.Span("Lattes", style={'color': 'white', 'fontWeight': 'bold'})
            ], style={'display': 'inline-block', 'width': '50%', 'textAlign': 'left', 'padding': '20px', 'fontSize': '190%',
                      'fontFamily': 'Arial'}),

            html.Div([html.Img(src='/assets/upe_logo_site.png', style={'width': '12%'})],
                     style={'display': 'inline-block', 'width': '50%', 'textAlign': 'right', 'padding': '10px'})
        ], style={'backgroundColor': '#001F3F', 'padding': '10px', 'display': 'flex', 'alignItems': 'center'}),

        html.Div([
            html.Div([
                html.P([
                    html.Strong("ExtratorLattes "),
                    "é uma plataforma desenvolvida para a visualização e análise de dados de docentes da Universidade de Pernambuco (UPE). Seu objetivo é facilitar o acesso a informações relevantes sobre a produção acadêmica, apoiando a avaliação da produtividade de programas de pós-graduação e grupos de pesquisa da instituição."
                ], style={
                    'textAlign': 'justify',
                    'color': 'white',
                    'fontSize': '16px',
                    'lineHeight': '1.6'
                }),

                html.Br(),

                html.Div([
                    html.A("Novo na plataforma? Clique aqui para visualizar o tutorial",
                           href="#",
                           id='open-tutorial-link',
                           style={
                               'color': 'white',
                               'fontWeight': 'bold',
                               'textDecoration': 'underline',
                               'cursor': 'pointer'
                           })
                ], style={'textAlign': 'center'})

            ], style={
                'backgroundColor': '#071B2D',
                'padding': '30px',
                'borderRadius': '10px',
                'width': '35%',
                'marginRight': '30px',
                'boxShadow': '0 4px 15px rgba(0,0,0,0.5)',
                'alignSelf': 'center'
            }),

            html.Div([
                dcc.Upload(
                    id='upload-researchers-data',
                    children=html.Button("Anexar arquivo .xlsx", id='btn-upload', style={
                        'backgroundColor': '#28a745',
                        'color': 'white',
                        'padding': '10px 20px',
                        'borderRadius': '10px',
                        'border': 'none',
                        'marginBottom': '10px',
                        'cursor': 'pointer',
                        'boxShadow': '0 4px 15px rgba(0,0,0,0.2)'
                    }),
                    multiple=False,
                    accept='.xlsx'
                ),
                html.Div(id='output-upload-status', style={'marginTop': '10px', 'color': 'white'}),

                html.Div("OU", style={'margin': '20px 0', 'fontWeight': 'bold', 'color': 'white'}),

                html.Button("Extrair do Sapiens", id='btn-sapiens', disabled=True, style={
                    'backgroundColor': '#6c757d',
                    'color': 'white',
                    'padding': '10px 20px',
                    'borderRadius': '10px',
                    'border': 'none',
                    'marginBottom': '10px',
                    'cursor': 'not-allowed',
                    'boxShadow': '0 4px 15px rgba(0,0,0,0.2)'
                }),

                html.Div([
                    html.Span("❗", style={'marginRight': '5px'}),
                    html.Span("Essa opção ainda não está disponível", style={'color': '#ddd'})
                ], style={'fontSize': '14px', 'marginTop': '5px'})
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center',
                'width': '45%',
                'alignSelf': 'center',
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'backgroundColor': '#6EA1C2',
            'padding': '10px 10px',
            'gap': '20px',
            'flexGrow': '1'
        })
    ], style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '90vh'}),

    html.Div(
        "©2025 Universidade de Pernambuco — Todos os direitos reservados",
        style={
            'backgroundColor': '#001F3F',
            'color': 'white',
            'padding': '30px',
            'textAlign': 'center',
            'fontSize': '14px'
        }
    ),
    html.Div(id="redirect-div-upload")
])

@callback(
    Output('redirect-div-upload', 'children'),
    Output('output-upload-status', 'children'),
    Output('store-uploaded-data', 'data'),
    Output('error-modal', 'is_open', allow_duplicate=True),
    Output('modal-error-message', 'children', allow_duplicate=True),
    Input('upload-researchers-data', 'contents'),
    State('upload-researchers-data', 'filename'),
    prevent_initial_call=True
)
def handle_upload(contents, filename):
    if contents is None:
        return no_update, no_update, no_update, no_update, no_update

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        xls = pd.ExcelFile(BytesIO(decoded))
        excel_data = {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}

        all_sheets_valid = True
        total_researchers = 0
        for sheet_name, df_sheet in excel_data.items():
            if 'id Lattes' not in df_sheet.columns or 'Docente' not in df_sheet.columns:
                all_sheets_valid = False
                break
            total_researchers += len(df_sheet)

        if not all_sheets_valid:
            return (
                no_update,
                'Erro: O arquivo Excel deve conter as colunas "id Lattes" e "Docente" em todas as abas.',
                no_update,
                True,
                "Erro: O arquivo Excel deve conter as colunas 'id Lattes' e 'Docente' em todas as abas."
            )

        data_to_store = {
            'filename': filename,
            'conteudo_base64': content_string
        }

        if 'PROGRAMAS' in excel_data:
            data_to_store['tipo'] = 'programas'
            for sheet_name, df_sheet in excel_data.items():
                if 'id Lattes' in df_sheet.columns:
                    ids_validos = (
                        df_sheet['id Lattes']
                        .dropna().astype(str).str.strip()
                        .loc[lambda x: x.str.match(r'^\d+$')]
                        .unique().tolist()
                    )
                    data_to_store[sheet_name] = ids_validos
        elif 'GRUPOS' in excel_data:
            data_to_store['tipo'] = 'grupos'
            for sheet_name, df_sheet in excel_data.items():
                if 'id Lattes' in df_sheet.columns:
                    ids_validos = (
                        df_sheet['id Lattes']
                        .dropna().astype(str).str.strip()
                        .loc[lambda x: x.str.match(r'^\d+$')]
                        .unique().tolist()
                    )
                    data_to_store[sheet_name] = ids_validos
        else:
            data_to_store['tipo'] = 'programas'
            all_ids = []
            for df_sheet in excel_data.values():
                if 'id Lattes' in df_sheet.columns:
                    ids_validos = (
                        df_sheet['id Lattes']
                        .dropna().astype(str).str.strip()
                        .loc[lambda x: x.str.match(r'^\d+$')]
                        .unique().tolist()
                    )
                    all_ids.extend(ids_validos)
            data_to_store['pesquisadores_gerais'] = all_ids

        status_message = f'Arquivo "{filename}" carregado com sucesso! ({total_researchers} pesquisadores em {len(excel_data)} abas).'

        return dcc.Location(pathname="/filtros", id="redirect-after-upload", refresh=True), status_message, data_to_store, False, ""

    except Exception as e:
        error_msg = f"Erro ao carregar arquivo: {e}"
        return no_update, 'Erro ao processar o arquivo. Certifique-se de que é um arquivo Excel válido.', no_update, True, error_msg