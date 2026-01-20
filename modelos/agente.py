from abc import ABC, abstractmethod


class Agente(ABC):
    def __init__(self, cenario):
        self.cenario = cenario
        self.posicao = self.cenario.jogador_pos
        self.pontos = 0

        self.inventario = {
            'flechas': self.cenario.qtd_wumpus,
            'ouro': 0
        }
        self.vivo = True
        self.qtdpassos = 0

    @abstractmethod

    def get_percepcao_atual(self):
       pass
    def decidir_acao(self):
       pass
    def status(self):
        jogo_status = self.cenario.checar_Agente(self.inventario)
        if jogo_status == "W":
            self.vivo = False
            print("O agente foi devorado pelo Wumpus!")
            self.pontos -= 1000
            return "W"
        elif jogo_status == "P":
            self.vivo = False
            self.pontos -= 1000
            print("O agente caiu em um poço!")
            return "P"
        elif jogo_status == "V":
            print("O agente venceu o jogo!")
            self.pontos += 1000
            return "V"
        else:
            print("O agente continua vivo e explorando o mundo.")
        