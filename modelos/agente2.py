from modelos.agente import Agente
from modelos.memoria import Memoria
from modelos.estrela import a_estrela, converter_direcao
import random

class Agente2(Agente):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.memoria = Memoria()
    
    def get_percepcao_atual(self):
        linha, coluna = self.cenario.jogador_pos
        return self.cenario.matrizPercp[linha][coluna]
    
    def decidir_acao(self):
        pos_atual = tuple(self.cenario.jogador_pos)
        percepcao = self.get_percepcao_atual()
        
       
        self.memoria.atualizar(pos_atual, percepcao, self.cenario.tamanho)
        obstaculos = self.memoria.get_obstaculos()
        
       
        if 'b' in percepcao:
            if self.cenario.pegar_ouro():
                self.inventario['ouro'] += 1
                self.pontos += 100
                self.cenario.matriz2()
                self.memoria.marcar_ouro_coletado(pos_atual)
        
        
        if 'f' in percepcao and self.inventario['flechas'] > 0:
            direcao_tiro = self._decidir_tiro(pos_atual)
            if direcao_tiro:
                return direcao_tiro

        
        if self.inventario['ouro'] > 0:
            caminho_volta = a_estrela(list(pos_atual), [0, 0], self.cenario, obstaculos=obstaculos)
            if caminho_volta and len(caminho_volta) > 1:
                return converter_direcao(caminho_volta[0], caminho_volta[1])

       
        objetivos = self.memoria.get_objetivos()
        for objetivo in objetivos:
            caminho = a_estrela(list(pos_atual), list(objetivo), self.cenario, obstaculos=obstaculos)
            if caminho and len(caminho) > 1:
                return converter_direcao(caminho[0], caminho[1])
        
        
        direcoes = self.cenario.direcoes_possiveis(self.cenario.jogador_pos)
        
        melhor_direcao = self.memoria.get_melhor_direcao(pos_atual, direcoes, self.cenario.tamanho)
        
        return melhor_direcao
    
    def _decidir_tiro(self, pos_atual):
        direcoes = self.cenario.direcoes_possiveis(self.cenario.jogador_pos)
        linha, coluna = pos_atual
        
        for direcao in direcoes:
            alvo = None
            if direcao == 'CIMA': alvo = (linha-1, coluna)
            elif direcao == 'BAIXO': alvo = (linha+1, coluna)
            elif direcao == 'ESQUERDA': alvo = (linha, coluna-1)
            elif direcao == 'DIREITA': alvo = (linha, coluna+1)
            
            if alvo and self.memoria.calcular_risco(alvo) >= 5:
                acertou = self.cenario.atirar_flecha(direcao)
                self.inventario['flechas'] -= 1
                if acertou:
                    self.pontos += 50
                    self.memoria.marcar_wumpus_morto(alvo)
                else:
                    self.pontos -= 10
                return direcao
        return None

    def reset_agente2(self):
        self.posicao = self.cenario.jogador_pos
        self.pontos = 0
        self.inventario = {'flechas': 3, 'ouro': 0}
        self.vivo = True
        self.qtdpassos = 0