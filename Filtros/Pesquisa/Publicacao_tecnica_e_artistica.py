import sys
import os

# Adicione o diretório raiz do seu projeto ao caminho de busca do Python
projeto_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(projeto_dir)

from Filtros.constantes_filtros import *
class Publicacao_tecnica_e_artistica():

    def __init__(self, titulo, periodico, issn, qualis, ano=None):

        self.titulo = titulo
        self.periodico = periodico
        self.issn = issn
        self.qualis = qualis
        self.peso = PESO_TECNICO_ARTISTICO
        self.ano = ano


