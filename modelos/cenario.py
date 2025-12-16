import pygame
import os
import random


class Cenario:
    def __init__(self, caminho_img, tamanho,tamanho_desenho):
        self.caminho_img = caminho_img
        self.tamanho_desenho = tamanho_desenho
        self.tamanho = tamanho
        self.tamanho_bloco = self.tamanho_desenho/self.tamanho
        self.jogador_pos = [0, 0]
        self.imagens = {}
        self.matriz = []
        self.matrizPercp = []
        self.criar_matriz()
        self.carregar_Img()
        self.quantPoco = tamanho-1
        self.qtdOuro = self.quantPoco - 1
        self.qtdWumpus = self.qtdOuro
        for _ in range(self.quantPoco):
            self.poco()
        for _ in range(self.qtdOuro):
            self.ouro()
        for _ in range(self.qtdWumpus):
            self.wumpus()
        self.matriz2()
        # Carregar imagens
        chao = pygame.image.load(caminho_img + r'\chao.png')
        chao = pygame.image.load(caminho_img + r'\chaoI.png')
        poco = pygame.image.load(caminho_img + r'\poço.png')
        wumpus = pygame.image.load(caminho_img + r'\wumpusV.png')
        wumpusM = pygame.image.load(caminho_img + r'\wumpusM.png')
        ouro = pygame.image.load(caminho_img + r'\ouro.png')
        jogador = pygame.image.load(caminho_img + r'\persona.png')

        # Ajustar tamanho para caber nas células
        chao = pygame.transform.scale(chao, (self.tamanho_bloco, self.tamanho_bloco))
        poco = pygame.transform.scale(poco, (self.tamanho_bloco, self.tamanho_bloco))
        wumpus = pygame.transform.scale(wumpus, (self.tamanho_bloco, self.tamanho_bloco))
        ouro = pygame.transform.scale(ouro, (self.tamanho_bloco, self.tamanho_bloco))
        jogador = pygame.transform.scale(jogador, (self.tamanho_bloco, self.tamanho_bloco))
        print(f"🎯 Cenário pronto! Mundo {self.tamanho}x{self.tamanho}")

    def criar_matriz(self):
        print(f"Criando matriz {self.tamanho}x{self.tamanho}")
        self.matriz = []
        for linha in range(self.tamanho):
            nova_linha = []
            for coluna in range(self.tamanho):
                if linha == 0 and coluna == 0:
                    nova_linha.append('I')
                else:
                    nova_linha.append('C')
            self.matriz.append(nova_linha)

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
        self.imagens['WM'] = pygame.transform.scale(
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

    def posicao_aleatoria(self):
        linhas = self.tamanho
        colunas = self.tamanho
        while True:
            linhas = random.randint(0, self.tamanho - 1)
            colunas = random.randint(0, self.tamanho - 1)
            if linhas != 0 and colunas != 0:
                return linhas, colunas

    def poco(self):
        while True:
            linha, coluna = self.posicao_aleatoria()
            if self.matriz[linha][coluna] == "C":
                self.matriz[linha][coluna] = "P"
                print(f" poco colocado em [{linha, coluna}]")
                break

    def ouro(self):
        while True:
            linha, coluna = self.posicao_aleatoria()
            if self.matriz[linha][coluna] == "C":
                self.matriz[linha][coluna] = "O"
                print(f"ouro colocado em[{linha, coluna}]")
                break

            elif self.matriz[linha][coluna] == "W":
                self.matriz[linha][coluna] = "W,O"
                print(f"ouro e wumpus adicionados em [{linha, coluna}] ")
                break

    def wumpus(self):
        while True:
            linha, coluna = self.posicao_aleatoria()
            if self.matriz[linha][coluna] == "C":
                self.matriz[linha][coluna] = "W"
                break
            elif self.matriz[linha][coluna] == "O":
                self.matriz[linha][coluna] = "W,O"
                break

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
        self.matriz = []
        self.matrizPercp = []

        self.criar_matriz()

        self.quantPoco = self.tamanho - 1
        self.qtdOuro = self.quantPoco - 1
        self.qtdWumpus = self.qtdOuro

        for _ in range(self.quantPoco):
            self.poco()
        for _ in range(self.qtdOuro):
            self.ouro()
        for _ in range(self.qtdWumpus):
            self.wumpus()

        self.matriz2()

        print("\n🔄 Mundo reiniciado!")
        print(f"Jogador na posição: {self.jogador_pos}")
