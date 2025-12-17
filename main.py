import pygame
from pygame.locals import QUIT
from sys import exit
from pathlib import Path
from modelos.cenario import Cenario
from modelos.botao import Botao

TAMANHO_JANELA = 700

pygame.init()
caminho = Path('img')
mundo = Cenario(caminho, tamanho=4, tamanho_desenho=TAMANHO_JANELA)


BG = pygame.transform.scale(
    pygame.image.load(Path('img').joinpath('menu_fundo.png')),
    (TAMANHO_JANELA, TAMANHO_JANELA)
)

tela = pygame.display.set_mode((TAMANHO_JANELA, TAMANHO_JANELA))


def get_font(tamanho_fonte):
    return pygame.font.SysFont("courier", tamanho_fonte, bold=True)


def menu():
    pygame.display.set_caption('Menu Principal')

    AGENTE1_BOTAO = Botao((350, 350), "AGENTE 1",
                          get_font(40), "#d7fcd4", "White")
    AGENTE2_BOTAO = Botao((350, 420), "AGENTE 2",
                          get_font(40), "#d7fcd4", "White")
    AGENTE3_BOTAO = Botao((350, 490), "AGENTE 3",
                          get_font(40), "#d7fcd4", "White")
    SAIR_BOTAO = Botao((350, 560), "SAIR", get_font(40), "#d7fcd4", "White")

    botoes = [AGENTE1_BOTAO, AGENTE2_BOTAO, AGENTE3_BOTAO, SAIR_BOTAO]

    while True:
        tela.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        for botao in botoes:
            botao.mudar_cor(MENU_MOUSE_POS)
            botao.atualizar(tela)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AGENTE1_BOTAO.verificar_entrada(MENU_MOUSE_POS):
                    jogo()
                    return 1
                if AGENTE2_BOTAO.verificar_entrada(MENU_MOUSE_POS):
                    print("AGENTE 2 SELECIONADO")
                    return 2
                if AGENTE3_BOTAO.verificar_entrada(MENU_MOUSE_POS):
                    print("AGENTE 3 SELECIONADO")
                    return 3
                if SAIR_BOTAO.verificar_entrada(MENU_MOUSE_POS):
                    pygame.quit()
                    exit()

        pygame.display.update()


def jogo():
    pygame.display.set_caption('MUNDO DE WUMPUS - JOGO')
    while True:
        tela.fill("black")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mundo.reset()

        mundo.desenhar(tela)
        pygame.display.update()


menu()
