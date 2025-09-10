from Filtros.constantes_filtros import *

class Publicacao_cientifica:

    def __init__(self, titulo, periodico, issn, qualis, ano=None):

        self.titulo = titulo
        self.periodico = periodico
        self.issn = issn
        self.qualis = qualis
        self.ano = ano
        self.peso = self.peso()


    def peso(self):

        peso = 0

        if self.qualis == 'A1':

            peso = QUALIS_A1

        elif self.qualis == 'A2':

            peso = QUALIS_A2

        elif self.qualis == 'A3':

            peso = QUALIS_A3

        elif self.qualis == 'A4':

            peso = QUALIS_A4

        elif self.qualis == 'B1':

            peso = QUALIS_B1

        elif self.qualis == 'B2':

            peso = QUALIS_B2

        elif self.qualis == 'B3':

            peso = QUALIS_B3

        elif self.qualis == 'B4':

            peso = QUALIS_B4

        return peso


        


        