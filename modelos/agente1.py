
from modelos.agente import Agente
import random


class Agente1(Agente):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.atirou = False

    def get_percepcao_atual(self):
        linha, coluna = self.cenario.jogador_pos
        return self.cenario.matrizPercp[linha][coluna]

    def decidir_acao(self):

        direcoes = self.cenario.direcoes_possiveis(self.cenario.jogador_pos)
        acao = random.choice(direcoes)

        if "b" in self.get_percepcao_atual():
            if self.cenario.pegar_ouro():
                self.inventario['ouro'] += 1
                self.pontos += 100
                self.cenario.matriz2()
        
        if "f" in self.get_percepcao_atual():
            if self.inventario['flechas'] > 0 and self.cenario.atirar_flecha(acao):
                self.inventario['flechas'] -= 1
                self.atirou = True
                
    
        return acao
