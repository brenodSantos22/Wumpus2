import pygame
from modelos.agente1 import Agente1
from modelos.agente import Agente
import os
import copy
from pathlib import Path
import random
Path.joinpath


class Cenario:
    def __init__(self, caminho_img:Path, tamanho,tamanho_desenho):
        self.caminho_img = caminho_img
        self.tamanho_desenho = tamanho_desenho
        self.tamanho = tamanho
        self.tamanho_bloco = self.tamanho_desenho/self.tamanho
        self.jogador_pos = [0, 0]
        self.qtd_wumpus =  0
        self.ouro_memoria = []
        self.imagens = {}
        self.matriz = []
        self.matrizPercp = []
        self.criar_matriz()
        self.carregar_Img()
        self.matriz2()
        self.matriz_original = copy.deepcopy(self.matriz)

        # Carregar imagens
        chao = pygame.image.load(caminho_img.joinpath("chao.png"))
        chaoI = pygame.image.load(caminho_img.joinpath('chaoI.png'))
        poco = pygame.image.load(caminho_img.joinpath("poço.png"))
        wumpus = pygame.image.load(caminho_img.joinpath("wumpusV.png"))
        wumpusM = pygame.image.load(caminho_img.joinpath("wumpusM.png"))
        ouro = pygame.image.load(caminho_img.joinpath("ouro.png"))
        jogador = pygame.image.load(caminho_img.joinpath("persona.png"))

        # Ajustar tamanho para caber nas células
        chao = pygame.transform.scale(chao, (self.tamanho_bloco, self.tamanho_bloco))
        chaoI = pygame.transform.scale(chaoI, (self.tamanho_bloco, self.tamanho_bloco))
        poco = pygame.transform.scale(poco, (self.tamanho_bloco, self.tamanho_bloco))
        wumpus = pygame.transform.scale(wumpus, (self.tamanho_bloco, self.tamanho_bloco))
        wumpusM = pygame.transform.scale(wumpusM, (self.tamanho_bloco, self.tamanho_bloco))
        ouro = pygame.transform.scale(ouro, (self.tamanho_bloco, self.tamanho_bloco))
        jogador = pygame.transform.scale(jogador, (self.tamanho_bloco, self.tamanho_bloco))

        print(f"🎯 Cenário pronto! Mundo {self.tamanho}x{self.tamanho}")

    def criar_matriz(self):
        print(f"Criando matriz {self.tamanho}x{self.tamanho}")
        tamanho = self.tamanho
        mundo = ["C"]*(self.tamanho*self.tamanho - 1)
        qtd_poco = tamanho-1
        qtd_wumpus = qtd_poco -1
        qtd_ouro = qtd_wumpus
        
        qtd_poco_acc = qtd_poco
        qtd_wumpus_acc = qtd_poco_acc + qtd_wumpus
        qtd_ouro_acc = 1
        
        for i in range(qtd_poco_acc):
            mundo[i] = "P"
        
        for i in range(qtd_poco_acc, qtd_wumpus_acc):
            mundo[i] = "W"
        
        for i in range( qtd_ouro_acc):
            mundo[i] = "O"
        
        random.shuffle(mundo)
        mundo2 = [[" " for _ in range(tamanho)] for _ in range(tamanho)]
        print(mundo)
        for n, a in enumerate(mundo, start=1):
            mundo2[n%tamanho][(int(n/tamanho))%tamanho] = a
        mundo2[0][0] = "I"
        self.matriz = mundo2


    def mover_jogador(self,direcoes):
        movimentos = {
            'CIMA': (-1, 0),
            'BAIXO': (1, 0),
            'ESQUERDA': (0, -1),
            'DIREITA': (0, 1),
        }
        dx, dy = movimentos[direcoes]
        self.jogador_pos[0] += dx
        self.jogador_pos[1] += dy

    def checar_Agente(self,inventario):
       linha, coluna = self.jogador_pos
       celula_atual = self.matriz[linha][coluna]
       devorado = "W" in celula_atual
       caiu = "P" in celula_atual
       ouro = "O" in celula_atual

       vitoria = False
       if (self.jogador_pos == [0, 0]) and (inventario['ouro'] > 0):
           vitoria = True

       if vitoria:
            return "V"
       elif devorado:
            return "W"
       elif caiu:
            return "P"
       else:
            return "-"
       
    def pegar_ouro(self):
        linha, coluna = self.jogador_pos
        celula_atual = self.matriz[linha][coluna]
        if "O" in celula_atual:
            self.matriz[linha][coluna] = self.matriz[linha][coluna].replace("O", "C")
            self.matriz2()
            return True
        return False

    def atirar_flecha(self, direcao):
        direcoes ={
            'CIMA': (-1, 0),
            'BAIXO': (1, 0),
            'ESQUERDA': (0, -1),
            'DIREITA': (0, 1),
        }
       
        posicao = self.jogador_pos
        wumpus = (
            posicao[0] + direcoes[direcao][0],
            posicao[1] + direcoes[direcao][1]
        )
        if "W" in self.matriz[wumpus[0]][wumpus[1]]:
            self.matriz[wumpus[0]][wumpus[1]] = self.matriz[wumpus[0]][wumpus[1]].replace("W", "D")
            return True
        return False
        



    def direcoes_possiveis(self,jogador_pos):
        direcoes = {
            'CIMA': (self.jogador_pos[0] - 1, self.jogador_pos[1]),
            'BAIXO': (self.jogador_pos[0] + 1, self.jogador_pos[1]),
            'ESQUERDA': (self.jogador_pos[0], self.jogador_pos[1] - 1),
            'DIREITA': (self.jogador_pos[0], self.jogador_pos[1] + 1)
        }

        reposta = []

        for direcao, (linha, coluna) in direcoes.items():
            if 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho:
                reposta.append(direcao)
        return reposta
        
    def carregar_Img(self):
        self.imagens['I'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'chaoI.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['C'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'chao.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['P'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'poço.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['W'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'wumpusV.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['D'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'wumpusM.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['O'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'ouro.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )
        self.imagens['J'] = pygame.transform.scale(
            pygame.image.load(os.path.join(self.caminho_img, 'persona.png')),
            (self.tamanho_bloco, self.tamanho_bloco)
        )

    def desenhar(self, tela, offset_x=0, offset_y=0):
        for linha in range(self.tamanho):
            for coluna in range(self.tamanho):
                x = offset_x + coluna * self.tamanho_bloco
                y = offset_y + linha * self.tamanho_bloco

                tipo_celula = self.matriz[linha][coluna]

        
                for simbolo in tipo_celula.split(','):
                    if simbolo in self.imagens:
                        tela.blit(self.imagens[simbolo], (x, y))
        jogador_x = offset_x + self.jogador_pos[1] * self.tamanho_bloco
        jogador_y = offset_y + self.jogador_pos[0] * self.tamanho_bloco
        jogador_img = pygame.transform.rotate(self.imagens['J'], 180)
        tela.blit(jogador_img, (jogador_x, jogador_y))
        
    def matriz2(self):
        self.matrizPercp = []
        for linha in range(self.tamanho):
            nova_linha = []
            for coluna in range(self.tamanho):
                nova_linha.append('')

            self.matrizPercp.append(nova_linha)

        for linha in range(self.tamanho):
            for coluna in range(self.tamanho):
                if "W" in self.matriz[linha][coluna]:
                    if linha - 1 > -1:
                        self.matrizPercp[linha-1][coluna] += "f"
                        self.matrizPercp[linha-1][coluna] = ",".join(
                            set(self.matrizPercp[linha-1][coluna]))
                    if linha+1 < self.tamanho:
                        self.matrizPercp[linha+1][coluna] += "f"
                        self.matrizPercp[linha+1][coluna] = ",".join(
                            set(self.matrizPercp[linha+1][coluna]))
                    if coluna - 1 > -1:
                        self.matrizPercp[linha][coluna-1] += "f"
                        self.matrizPercp[linha][coluna-1] = ",".join(
                            set(self.matrizPercp[linha][coluna-1]))
                    if coluna+1 < self.tamanho:
                        self.matrizPercp[linha][coluna+1] += "f"
                        self.matrizPercp[linha][coluna+1] = ",".join(
                            set(self.matrizPercp[linha][coluna+1]))

                if "P" in self.matriz[linha][coluna]:
                    if linha - 1 > -1:
                        self.matrizPercp[linha-1][coluna] += "v"
                        self.matrizPercp[linha-1][coluna] = ",".join(
                            set(self.matrizPercp[linha-1][coluna]))
                    if linha+1 < self.tamanho:
                        self.matrizPercp[linha+1][coluna] += "v"
                        self.matrizPercp[linha+1][coluna] = ",".join(
                            set(self.matrizPercp[linha+1][coluna]))
                    if coluna - 1 > -1:
                        self.matrizPercp[linha][coluna-1] += "v"
                        self.matrizPercp[linha][coluna-1] = ",".join(
                            set(self.matrizPercp[linha][coluna-1]))
                    if coluna+1 < self.tamanho:
                        self.matrizPercp[linha][coluna+1] += "v"
                        self.matrizPercp[linha][coluna+1] = ",".join(
                            set(self.matrizPercp[linha][coluna+1]))

                if "O" in self.matriz[linha][coluna]:
                    self.matrizPercp[linha][coluna] += "b"
                    self.matrizPercp[linha][coluna] = ",".join(
                    set(self.matrizPercp[linha][coluna]))
        

    def reset(self):

        self.jogador_pos = [0, 0]
        self.matriz = copy.deepcopy(self.matriz_original)
        self.matriz2()

        print("\n Mundo reiniciado!")
        print(f"Jogador na posição: {self.jogador_pos}")
