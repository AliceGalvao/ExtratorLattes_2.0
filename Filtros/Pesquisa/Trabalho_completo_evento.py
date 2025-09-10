from Filtros.constantes_filtros import *

class Trabalho_completo_evento:

    def __init__(self, titulo, natureza, nome_evento, titulo_dos_anais, ano=None):

        self.titulo = titulo
        self.natureza = natureza
        self.nome_evento = nome_evento
        self.titulo_dos_anais = titulo_dos_anais
        self.peso = PESO_PUBLICACAO_TRABALHO_EVENTO
        self.ano = ano

    
        

