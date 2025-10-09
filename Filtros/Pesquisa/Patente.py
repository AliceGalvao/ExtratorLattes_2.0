from Filtros.constantes_filtros import *

class Patente:

    def __init__(self, tipo, titulo, codigo, instituicao_deposito_registro, data_concessao):
        
        self.tipo = tipo
        self.titulo = titulo
        self.codigo = codigo
        self.instituicao_deposito_registro = instituicao_deposito_registro
        self.data_concessao = data_concessao
