import sys
import os
from re import search
from wsgiref.simple_server import software_version

import pandas as pd

# Adicione o diretório raiz do seu projeto ao caminho de busca do Python
projeto_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(projeto_dir)

import xml.etree.ElementTree as ET
from Filtros.Ensino import Orientacao
from Filtros.Pesquisa import Trabalho_completo_evento
from Filtros.Pesquisa import Patente
from Filtros.Pesquisa import Software
from Filtros.Pesquisa import Publicacao_livro_ISBN
from Filtros.Pesquisa import Publicacao_capitulo_ISBN
from Filtros.Pesquisa import Publicacao_cientifica
from Filtros.Pesquisa import Publicacao_tecnica_e_artistica
from Filtros.Pesquisa import Projeto
from Filtros import Organizacao_eventos
from Read_Data.constants import *
from Filtros.constantes_filtros import *
#from dotenv import load_dotenv #carregar as variáveis de ambiente


class Leitor_xml:

    def __init__(self, xml, ano_inicio=None, ano_termino=None):

        self.curriculo = ET.parse(xml)
        self.root = self.curriculo.getroot()
        self.ano_inicio = ano_inicio
        self.ano_termino = ano_termino

    def _filtro_ano(self, ano):
        if not ano:
            return False
        try:
            ano_int = int(ano)
        except:
            return False
        if self.ano_inicio and ano_int < self.ano_inicio:
            return True
        if self.ano_termino and ano_int > self.ano_termino:
            return True
        return False

    def extrair_nome_id_bolsista(self, id_vazio):

        dados_gerais = self.root.find(DADOS_GERAIS)
        nome_completo = dados_gerais.get(NOME_COMPLETO)
        id = self.root.get(NUMERO_IDENTIFICADOR)
        planilha_bolsistas = pd.read_csv('./Read_Data/static/PLANILHA_BOLSISTAS.csv')

        #obtendo ano de titulação do doutorado
        formacao_academica_titulacao = dados_gerais.find(FORMACAO_ACADEMICA_TITULACAO)
        titulacao_doutorado = formacao_academica_titulacao.find(TITULACAO_DOUTORADO)
        if titulacao_doutorado != None:
            ano_titulacao_doutorado = titulacao_doutorado.get(ANO_TITULACAO)
        else:
            ano_titulacao_doutorado = None

        if id == '' or id == None:
            id = id_vazio

        if int(id) in list(planilha_bolsistas['ID']):
            bolsista = True
            categoria_bolsa = planilha_bolsistas.loc[planilha_bolsistas['ID'] == int(id)]['CATEGORIA_BOLSA'].unique()[0]
            return [nome_completo, id, bolsista, categoria_bolsa, ano_titulacao_doutorado]

        else:

            return [nome_completo, id, False, None, ano_titulacao_doutorado]


    def extrair_orientacao(self, child, f1, f2, concluido):

        orientacoes = list()

        for child in self.root.iter(child):

            detalhamento = child.find(f1)

            if detalhamento != None:
                cods_instituicao = detalhamento.get(CODIGO_INSTITUICAO)
                nome_instituicao = detalhamento.get(NOME_INSTITUICAO)
                curso = detalhamento.get(CURSO)
                tipo_orientacao = detalhamento.get(TIPO_ORIENTACAO)

                dados = child.find(f2)
                ano = dados.get(ANO)
                titulo = dados.get(TITULO)
                natureza = dados.get(NATUREZA)

                if self._filtro_ano(ano):
                    continue

                orientacoes.append(Orientacao.Orientacao(titulo, concluido, natureza, tipo_orientacao, cods_instituicao, nome_instituicao, curso, ano))

        return orientacoes


    def extrair_orientacao_ic(self, child, f1, f2, concluido):

        orientacoes_ic = list()

        for child in self.root.iter(child):

            dados = child.find(f2)
            natureza = dados.get(NATUREZA)

            detalhamento = child.find(f1)
            tipo_orientacao = detalhamento.get(TIPO_ORIENTACAO_IC)

            if ((natureza == DESCRICAO_IC1) | (natureza == DESCRICAO_IC2)): #& (tipo_orientacao == ORIENTADOR_PRINCIPAL):

                titulo = dados.get(TITULO)

                cods_instituicao = detalhamento.get(CODIGO_INSTITUICAO)
                nome_instituicao = detalhamento.get(NOME_INSTITUICAO)
                curso = detalhamento.get(CURSO)
                ano = dados.get(ANO)

                if self._filtro_ano(ano):
                    continue

                orientacoes_ic.append(Orientacao.Orientacao(titulo, concluido, natureza, tipo_orientacao, cods_instituicao, nome_instituicao, curso, ano))

        return orientacoes_ic


    def extrair_trabalho_completo_evento(self, child, f1, f2):

        trabalhos = list()

        for child in self.root.iter(child):

            dados = child.find(f1)
            titulo = dados.get(TITULO_TRABALHO)
            natureza = dados.get(NATUREZA)

            if natureza == 'COMPLETO':

                detalhamento = child.find(f2)
                nome_evento = detalhamento.get(NOME_DO_EVENTO)
                titulo_anais = detalhamento.get(TITULO_DOS_ANAIS)
                ano = dados.get(ANO_TRABALHO)

                if self._filtro_ano(ano):
                    continue

                trabalhos.append(Trabalho_completo_evento.Trabalho_completo_evento(titulo, natureza, nome_evento, titulo_anais, ano))

        return trabalhos


    def extrair_patentes(self, child, f1):
        patentes = list()
        for child in self.root.iter(child):
            tipo = child.get(TIPO_PATENTE)
            if tipo == PATENTE_SOFTWARE:
                continue

            data_pedido = child.get(DATA_PEDIDO_PATENTE)
            ano_pedido = None
            if data_pedido and len(data_pedido) >= 4:
                ano_pedido = data_pedido[-4:]

            if self._filtro_ano(ano_pedido):
                continue

            titulo = child.get(TITULO_PATENTE)
            codigo = child.get(CODIGO_PATENTE)
            instituicao = child.get(INSTITUICAO_REGISTRO_DEPOSITO)
            patentes.append(Patente.Patente(tipo, titulo, codigo, instituicao, data_pedido))
        return patentes

    def extrair_softwares(self, child, f1):
        softwares = list()
        for child in self.root.iter(child):
            tipo = child.get(TIPO_PATENTE)
            if tipo != PATENTE_SOFTWARE:
                continue
            data_pedido = child.get(DATA_PEDIDO_PATENTE)
            ano_pedido = None
            if data_pedido and len(data_pedido) >= 4:
                ano_pedido = data_pedido[-4:]

            if self._filtro_ano(ano_pedido):
                continue

            titulo = child.get(TITULO_PATENTE)
            codigo = child.get(CODIGO_PATENTE)
            instituicao = child.get(INSTITUICAO_REGISTRO_DEPOSITO)
            softwares.append(Software.Software(tipo, titulo, codigo, instituicao, data_pedido))
        return softwares

    def extrair_livro_ISBN(self,child, f1, f2):

        livros_isbn = list()

        for child in self.root.iter(child):

            detalhamento = child.find(f2)
            isbn = detalhamento.get(ISBN)

            if isbn != None:

                dados = child.find(f1)
                titulo = dados.get(TITULO_DO_LIVRO)
                tipo = dados.get(TIPO)
                ano = dados.get(ANO)

                if self._filtro_ano(ano):
                    continue

                livros_isbn.append(Publicacao_livro_ISBN.Publicacao_livro_ISBN(titulo, tipo, isbn, ano))

        return livros_isbn


    def extrair_capitulo_ISBN(self, child, f1, f2):

        capitulos_isbn = list()

        for child in self.root.iter(child):

            detalhamento = child.find(f2)
            isbn = detalhamento.get(ISBN)

            if isbn != None:

                dados = child.find(f1)
                titulo_capitulo = dados.get(TITULO_DO_CAPITULO)
                titulo_livro = detalhamento.get(TITULO_DO_LIVRO)
                tipo = dados.get(TIPO)
                ano = dados.get(ANO)

                if self._filtro_ano(ano):
                    continue

                capitulos_isbn.append(Publicacao_capitulo_ISBN.Publicacao_capitulo_ISBN(titulo_capitulo, titulo_livro, tipo, isbn, ano))

        return capitulos_isbn


    def extrair_artigos(self, child, f1, f2):

        artigos = list()
        qualis_geral = pd.read_csv('./Read_Data/static/qualis_geral.csv')

        for child in self.root.iter(child):

            detalhamento = child.find(f2)
            issn = detalhamento.get(ISSN)

            if ((issn != None) & (issn in list(qualis_geral['ISSN']))):

                qualis = qualis_geral.loc[qualis_geral['ISSN'] == issn]['Estrato'].unique()[0]

                dados = child.find(f1)
                titulo = dados.get(TITULO_DO_ARTIGO)
                periodico = detalhamento.get(TITULO_PERIODICO)
                ano = dados.get(ANO_ARTIGO)

                if self._filtro_ano(ano):
                    continue

                if qualis in LISTA_QUALIS:
                    artigos.append(Publicacao_cientifica.Publicacao_cientifica(titulo, periodico, issn, qualis, ano))

        return artigos


    def extrair_tecnico_artistico(self, child, f1, f2):

        tecnicos_e_artisticos = list()
        qualis_geral = pd.read_csv('./Read_Data/static/qualis_geral.csv')

        for child in self.root.iter(child):

            detalhamento = child.find(f2)
            issn = detalhamento.get(ISSN)

            if ((issn != None) & (issn in list(qualis_geral['ISSN']))):

                qualis = qualis_geral.loc[qualis_geral['ISSN'] == issn]['Estrato'].unique()[0]

                if qualis == 'C':

                    dados = child.find(f1)
                    titulo = dados.get(TITULO_DO_ARTIGO)
                    periodico = detalhamento.get(TITULO_PERIODICO)
                    ano = dados.get(ANO_ARTIGO)

                    if self._filtro_ano(ano):
                        continue

                    tecnicos_e_artisticos.append(Publicacao_tecnica_e_artistica.Publicacao_tecnica_e_artistica(titulo, periodico, issn, qualis, ano))

        return tecnicos_e_artisticos


    def extrair_eventos_organizados(self, child, f1):

        eventos_organizados = []

        for child in self.root.iter(child):

            dados = child.find(f1)
            tipo_evento = dados.get(TIPO_EVENTO)
            titulo_evento = dados.get(TITULO_EVENTO)
            ano_evento = dados.get(ANO)

            if self._filtro_ano(ano_evento):
                continue

            eventos_organizados.append(Organizacao_eventos.Organizacao_eventos(titulo_evento, tipo_evento, ano_evento))

        return eventos_organizados


    def extrair_projetos(self, child, f1):

        projetos = []

        for projeto in self.root.iter(child):

            ano = projeto.get(ANO_PROJETO)

            if self._filtro_ano(ano):
                continue

            natureza = projeto.get(NATUREZA_PROJETO)
            if natureza == f1:

                nome = projeto.get(NOME_PROJETO)
                situacao = projeto.get(SITUACAO_PROJETO)
                descricao = projeto.get(DESCRICAO_PROJETO)
                projetos.append(Projeto.Projeto(nome, natureza, descricao, situacao, ano))

        return projetos
