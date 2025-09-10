from  Filtros.Pesquisa import Publicacao_livro_ISBN
from Filtros.constantes_filtros import *

class Publicacao_capitulo_ISBN(Publicacao_livro_ISBN.Publicacao_livro_ISBN):

    def __init__(self, titulo, titulo_do_livro, tipo, isbn, ano=None):

        super().__init__(titulo, tipo, isbn)
        self.titulo_do_livro = titulo_do_livro
        self.peso = PESO_PUBLICACAO_CAPITULO_ISBN
        self.ano = ano


