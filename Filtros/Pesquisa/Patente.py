from Filtros.constantes_filtros import *

class Patente:

    def __init__(self, tipo, titulo, codigo, instituicao_deposito_registro, data_concessao):
        
        self.tipo = tipo
        self.titulo = titulo
        self.codigo = codigo
        self.instituicao_deposito_registro = instituicao_deposito_registro
        self.data_concessao = data_concessao
        self.ano = data_concessao[4:]
        self.peso = self.peso()


    def peso(self):

        if self.data_concessao != None:

            peso = PESO_REGISTRO_DE_PATENTE

        else:

            peso = PESO_DEPOSITO_DE_PATENTE

        return peso

    

    