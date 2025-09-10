from Filtros.constantes_filtros import *

class Publicacao_livro_ISBN:

    def __init__(self, titulo, tipo, isbn, ano=None):

        self.titulo = titulo
        self.tipo = tipo
        self.isbn = isbn
        self.peso = PESO_PUBLICACAO_LIVRO_ISBN
        self.ano = ano

