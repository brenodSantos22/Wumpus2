import pygame
from pygame.locals import QUIT
from sys import exit
from pathlib import Path
from modelos.cenario import Cenario


TAMANHO_JANELA = 700

pygame.init()
caminho = Path('img')
mundo = Cenario(caminho, tamanho=4, tamanho_desenho=TAMANHO_JANELA)

tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))
pygame.display.set_caption('MUNDO DE WUMPUS')

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        # Resetar com tecla R
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mundo.reset()

    tela.fill((0, 0, 0))
    mundo.desenhar(tela)
    pygame.display.update()
