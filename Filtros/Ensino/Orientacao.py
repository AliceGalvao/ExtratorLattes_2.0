from Filtros.constantes_filtros import * 

class Orientacao:

    def __init__(self, titulo, concluido, natureza, tipo_orientacao, cod_instituicao, nome_instituicao, curso, ano=None):
        
        self.titulo = titulo
        self.concluido = concluido
        self.natureza = natureza
        self.tipo_orientacao = tipo_orientacao
        self.cod_instituicao = cod_instituicao
        self.nome_instituicao = nome_instituicao
        self.curso = curso
        self.ano = ano
        self.peso = self.peso()

    def peso(self):

        if self.natureza == DESCRICAO_MESTRADO:

            if self.tipo_orientacao == ORIENTADOR_PRINCIPAL:

                if self.concluido == True:

                    return PESO_OP_MESTRADO_CONCLUIDO
                
                else:

                    return PESO_OP_MESTRADO_EM_ANDAMENTO

            elif self.tipo_orientacao == CO_ORIENTADOR:

         
                if self.concluido == True:

                    return PESO_CO_MESTRADO_CONCLUIDO
                 
                else:
                
                    return PESO_CO_MESTRADO_EM_ANDAMENTO

        elif self.natureza == DESCRICAO_DOUTORADO:

            if self.tipo_orientacao == ORIENTADOR_PRINCIPAL:

                if self.concluido == True:

                    return PESO_OP_DOUTORADO_CONCLUIDO
                
                else:

                    return PESO_OP_DOUTORADO_EM_ANDAMENTO

            elif self.tipo_orientacao == CO_ORIENTADOR:

         
                if self.concluido == True:

                    return PESO_CO_DOUTORADO_CONCLUIDO
                
                else:
                
                    return PESO_CO_DOUTORADO_EM_ANDAMENTO
                
        elif ((self.natureza == DESCRICAO_IC1) | (self.natureza == DESCRICAO_IC2)):

            return ORIENTACAO_EM_IC
      
        else:

            return 0



