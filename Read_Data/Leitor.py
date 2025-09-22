import os
import pandas as pd
import sys
import shutil
import traceback
import logging

projeto_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(projeto_dir)

from constants import *
from Leitor_xml import Leitor_xml
from Entidades.Pesquisador import Pesquisador

logger = logging.getLogger('dash_app')

class Leitor:

    def __init__(self):
        os.makedirs(PASTA_PROGRAMAS, exist_ok=True)
        download_path = None

    def le_programas(self):
        # lê os programas existentes
        with open('./programas.txt', 'r') as arquivo:
            programas = arquivo.read()
        PROGRAMAS = programas.split(',')

        # verifica estrutura de pastas
        for programa in PROGRAMAS:
            name_file = os.path.join(PASTA_PROGRAMAS, programa)
            if not os.path.exists(name_file):
                os.makedirs(name_file, exist_ok=True)
                logger.info(f'[.] A pasta {programa} foi criada')
            else:
                logger.info(f'[.] A pasta {programa} existe')

    def read_pesquisador(self, xml, ano_inicio=None, ano_termino=None):
        leitor_xml = Leitor_xml(xml, ano_inicio, ano_termino)
        id = os.path.basename(xml).split('.')[0]

        # eixo Ensino
        nome_e_id_bolsista = leitor_xml.extrair_nome_id_bolsista(id)
        orientacoes_mestrado_concluidas = leitor_xml.extrair_orientacao(
            ORIENTACOES_CONCLUIDAS_PARA_MESTRADO,
            DETALHAMENTO_DE_ORIENTACOES_CONCLUIDAS_PARA_MESTRADO,
            DADOS_BASICOS_DE_ORIENTACOES_CONCLUIDAS_PARA_MESTRADO, True
        )
        orientacoes_mestrado_andamento = leitor_xml.extrair_orientacao(
            ORIENTACOES_EM_ANDAMENTO_MESTRADO,
            DETALHAMENTO_DA_ORIENTACAO_EM_ANDAMENTO_DE_MESTRADO,
            DADOS_BASICOS_DA_ORIENTACAO_EM_ANDAMENTO_DE_MESTRADO, False
        )
        orientacoes_doutorado_concluidas = leitor_xml.extrair_orientacao(
            ORIENTACOES_CONCLUIDAS_PARA_DOUTORADO,
            DETALHAMENTO_DE_ORIENTACOES_CONCLUIDAS_PARA_DOUTORADO,
            DADOS_BASICOS_DE_ORIENTACOES_CONCLUIDAS_PARA_DOUTORADO, True
        )
        orientacoes_doutorado_andamento = leitor_xml.extrair_orientacao(
            ORIENTACOES_EM_ANDAMENTO_DOUTORADO,
            DETALHAMENTO_DA_ORIENTACAO_EM_ANDAMENTO_DE_DOUTORADO,
            DADOS_BASICOS_DA_ORIENTACAO_EM_ANDAMENTO_DE_DOUTORADO, False
        )

        # eixo Pesquisa
        trabalhos_eventos = leitor_xml.extrair_trabalho_completo_evento(
            TRABALHO_EM_EVENTOS, DADOS_BASICOS_DO_TRABALHO, DETALHAMENTO_DO_TRABALHO
        )
        patentes = leitor_xml.extrair_patentes(REGISTRO_OU_PATENTE, None)
        livros_ISBN = leitor_xml.extrair_livro_ISBN(LIVRO_PUBLICADO, DADOS_BASICOS_DO_LIVRO, DETALHAMENTO_DO_LIVRO)
        capitulos_ISBN = leitor_xml.extrair_capitulo_ISBN(
            CAPITULO_DE_LIVRO_PUBLICADO, DADOS_BASICOS_DO_CAPITULO, DETALHAMENTO_DO_CAPITULO
        )
        artigos_publicados = leitor_xml.extrair_artigos(
            ARTIGO_PUBLICADO, DADOS_BASICOS_DO_ARTIGO, DETALHAMENTO_DO_ARTIGO
        )
        orientacoes_ic_concluidas = leitor_xml.extrair_orientacao_ic(
            OUTRAS_ORIENTACOES_CONCLUIDAS, DETALHAMENTO_DE_OUTRAS_ORIENTACOES_CONCLUIDAS, DADOS_BASICOS_DE_OUTRAS_ORIENTACOES_CONCLUIDAS, True
        )
        orientacoes_ic_andamento = leitor_xml.extrair_orientacao_ic(
            IC_ANDAMENTO, DETALHAMENTO_IC_ANDAMENTO, DADOS_IC_ANDAMENTO, False
        )
        tecnicos_artisticos_nao_indexados = leitor_xml.extrair_tecnico_artistico(
            ARTIGO_PUBLICADO, DADOS_BASICOS_DO_ARTIGO, DETALHAMENTO_DO_ARTIGO
        )

        # eventos organizados
        eventos_organizados = leitor_xml.extrair_eventos_organizados(
            ORGANIZACAO_DE_EVENTO, DADOS_BASICOS_DA_ORGANIZACAO_DE_EVENTO
        )

        # projetos
        projetos_pesquisa = leitor_xml.extrair_projetos(PROJETO, PROJETO_PESQUISA)
        projetos_desenvolvimento = leitor_xml.extrair_projetos(PROJETO, PROJETO_DESENVOLVIMENTO)

        # registros de software
        registros_software = leitor_xml.extrair_patentes(REGISTRO_OU_PATENTE, PATENTE_SOFTWARE)

        # cria pesquisador e define atributos
        pesquisador = Pesquisador(
            nome_e_id_bolsista[0],
            nome_e_id_bolsista[1],
            nome_e_id_bolsista[2],
            nome_e_id_bolsista[3],
            nome_e_id_bolsista[4]
        )
        pesquisador.orientacoes_mestrado = orientacoes_mestrado_concluidas + orientacoes_mestrado_andamento
        pesquisador.orientacoes_doutorado = orientacoes_doutorado_concluidas + orientacoes_doutorado_andamento
        pesquisador.publicacoes_trabalhos_eventos = trabalhos_eventos
        pesquisador.patentes = patentes
        pesquisador.publicacoes_livros_ISBN = livros_ISBN
        pesquisador.publicacoes_capitulos_ISBN = capitulos_ISBN
        pesquisador.publicacoes_cientificas = artigos_publicados
        pesquisador.orientacoes_ic = orientacoes_ic_concluidas + orientacoes_ic_andamento
        pesquisador.publicacoes_tecnicas_e_artisticas = tecnicos_artisticos_nao_indexados
        pesquisador.eventos_organizados = eventos_organizados
        pesquisador.projetos_pesquisa = projetos_pesquisa
        pesquisador.projetos_desenvolvimento = projetos_desenvolvimento
        pesquisador.registros_software = registros_software

        return pesquisador

    def listar_arquivos_em_pasta(self, caminho_da_pasta):
        try:
            itens = os.listdir(caminho_da_pasta)
            arquivos_xml = [
                item for item in itens
                if os.path.isfile(os.path.join(caminho_da_pasta, item)) and item.lower().endswith('.xml')
            ]
            return arquivos_xml
        except OSError as e:
            logger.error(f"[X] Ocorreu um erro: {e}")
            return []

    def checa_organizacao_evento(self, pesquisadores):
        eventos_programa = []
        for pesquisador in pesquisadores:
            for evento in pesquisador.eventos_organizados:
                titulo = evento.titulo.lower().strip()
                ano = evento.ano
                eventos_programa.append((titulo, ano))
        return set(eventos_programa)

    def read_pesquisadores_programas(self, programa: str, ano_inicio=None, ano_termino=None):
        pesquisadores = []
        name_file = os.path.join(PASTA_PROGRAMAS, programa)

        if os.path.isdir(name_file):
            arquivos_xml = self.listar_arquivos_em_pasta(name_file)
            logger.info(f"[.] {len(arquivos_xml)} ARQUIVOS LISTADOS NA PASTA {name_file}")

            for arquivo in arquivos_xml:
                xml = os.path.join(name_file, arquivo)
                try:
                    pesquisador = self.read_pesquisador(xml, ano_inicio, ano_termino)
                    pesquisadores.append(pesquisador)
                except Exception as e:
                    logger.error(f'[X] Erro ao ler pesquisador {arquivo}: {str(e)}')
        else:
            logger.warning(f'[X] A pasta do programa não existe: {name_file}')

        return pesquisadores

    def read_pesquisadores_grupos(self, grupo: str):
        pesquisadores = []
        name_file = os.path.join(PASTA_GRUPOS, grupo)

        if os.path.isdir(name_file):
            arquivos_xml = self.listar_arquivos_em_pasta(name_file)
            for arquivo in arquivos_xml:
                pesquisador = self.read_pesquisador(os.path.join(name_file, arquivo))
                pesquisadores.append(pesquisador)
        else:
            logger.warning(f'[X] A pasta do grupo não existe: {name_file}')

        return pesquisadores

    def gerar_estrutura_de_csv_programas(self, ano_inicio=None, ano_termino=None, metricas=None):
        try:
            lista_dfs = []
            programas_totais = []
            programas_totais_eventos = []

            if os.path.exists(PASTA_PROGRAMAS):
                programas = os.listdir(PASTA_PROGRAMAS)
            else:
                programas = []

            if not programas:
                logger.error('[X] NÃO EXISTEM PROGRAMAS A PERCORRER')
                return None

            for programa in programas:
                pesquisadores_programa = self.read_pesquisadores_programas(programa, ano_inicio, ano_termino)
                eventos_organizados = self.checa_organizacao_evento(pesquisadores_programa)

                if not pesquisadores_programa:
                    logger.warning(f'[X] Não há pesquisadores no programa {programa}')
                    continue

                # dados individuais
                dados_pesquisadores = [p.series_eixo_ensino() for p in pesquisadores_programa]
                df = pd.DataFrame(dados_pesquisadores)
                df = df.loc[:, ~df.columns.duplicated()]

                # linha de totais
                linha_programa = {col: df[col].sum() for col in df.columns if df[col].dtype in [int, float]}
                linha_programa['Nome'] = programa
                linha_programa['ID LATTES'] = 'Não possui'
                df_totais = pd.DataFrame([linha_programa])

                # concatena e garante colunas únicas
                df_concat = pd.concat([df, df_totais], ignore_index=True)
                df_concat = df_concat.loc[:, ~df_concat.columns.duplicated()]

                # aplica filtro de métricas
                if metricas:
                    cols = ['Nome', 'ID LATTES'] + metricas
                    if 'PUBLICAÇÕES CIENTÍFICAS' in metricas:
                        cols += LISTA_QUALIS
                    df_concat = df_concat.loc[:, [c for c in cols if c in df_concat.columns]]

                lista_dfs.append([programa, df_concat])

                # totais gerais
                programas_totais.append(linha_programa)
                programas_totais_eventos.append({'Nome': programa, 'Quantidade de Eventos': len(eventos_organizados)})

            # aba total
            df_total = pd.DataFrame(programas_totais)

            # linha de soma (total geral)
            linha_soma = df_total.drop(columns=['Nome', 'ID LATTES'], errors='ignore').sum(numeric_only=True)
            linha_soma['Nome'] = 'Total Geral'
            linha_soma['ID LATTES'] = 'Não possui'

            # concatena df_total com a linha de soma **no final**
            df_total = pd.concat([df_total, pd.DataFrame([linha_soma])], ignore_index=True)

            # força a ordem das colunas: Nome e ID LATTES primeiro
            colunas = ['Nome', 'ID LATTES'] + [c for c in df_total.columns if c not in ['Nome', 'ID LATTES']]
            df_total = df_total[colunas]

            lista_dfs.append(['total', df_total])

            dict_retorno = {df[0]: df[1].to_json(orient='split') for df in lista_dfs}

            # limpa pasta programas
            if os.path.exists(PASTA_PROGRAMAS):
                shutil.rmtree(PASTA_PROGRAMAS)

            return dict_retorno

        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            logger.error(f"[X] ERRO AO GERAR ESTRUTURA DE PLANILHA: {traceback.format_exception(exc_type, exc_value, exc_tb)}")
            return None


    def gerar_estrutura_de_csv_grupos(self):
        df_grupo = pd.read_excel('./Read_Data/id_nome_grupo.xlsx')
        grupos_totais = []
        grupos_totais_eventos = []

        if not os.path.exists(PASTA_DADOS_SALVOS_GRUPOS):
            os.makedirs(PASTA_DADOS_SALVOS_GRUPOS)

        if os.path.exists(PASTA_GRUPOS):
            grupos = os.listdir(PASTA_GRUPOS)
        else:
            grupos = []

        if not grupos:
            logger.error('NÃO EXISTEM GRUPOS A PERCORRER')
            return None

        for grupo in grupos:
            nome_grupo = df_grupo.loc[df_grupo["id"] == int(grupo), "nome"].unique()[0]
            pesquisadores_grupo = self.read_pesquisadores_grupos(grupo)
            eventos_organizados = self.checa_organizacao_evento(pesquisadores_grupo)

            if not pesquisadores_grupo:
                logger.warning(f'[X] Não há pesquisadores no grupo {nome_grupo} de id {grupo}')
                continue

            dados_pesquisadores = [p.series_eixo_ensino() for p in pesquisadores_grupo]
            df = pd.DataFrame(dados_pesquisadores)
            df = df.loc[:, ~df.columns.duplicated()]

            linha_grupo = {col: df[col].sum() for col in df.columns if df[col].dtype in [int, float]}
            linha_grupo['Nome'] = nome_grupo
            linha_grupo['ID LATTES'] = grupo
            df_totais = pd.DataFrame([linha_grupo])

            df_concat = pd.concat([df, df_totais], ignore_index=True)
            df_concat = df_concat.loc[:, ~df_concat.columns.duplicated()]

            diretorio = os.path.join(PASTA_DADOS_SALVOS_GRUPOS, grupo)
            os.makedirs(diretorio, exist_ok=True)
            df_concat.to_excel(os.path.join(diretorio, f'{grupo}.xlsx'))

            grupos_totais.append(linha_grupo)
            grupos_totais_eventos.append({'Nome': nome_grupo, 'Quantidade de eventos': len(eventos_organizados)})

        # Totais gerais
        df_total_eventos = pd.DataFrame(grupos_totais_eventos)
        df_total_eventos.to_excel(os.path.join(PASTA_DADOS_SALVOS_GRUPOS, 'total_grupos_eventos.xlsx'))

        df_total = pd.DataFrame(grupos_totais)
        linha_soma = df_total.drop(columns=['Nome', 'ID LATTES'], errors='ignore').sum(numeric_only=True)
        linha_soma['Nome'] = 'Total Geral'
        linha_soma['ID LATTES'] = 'Não possui'
        df_total = pd.concat([pd.DataFrame([linha_soma]), df_total], ignore_index=True)
        df_total.to_excel(os.path.join(PASTA_DADOS_SALVOS_GRUPOS, 'total_grupos.xlsx'))
