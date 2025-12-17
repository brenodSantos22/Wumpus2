import pygame

class Botao:
    def __init__(self, pos, texto, fonte, cor_base, cor_passe_mouse):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.fonte = fonte
        self.cor_base = cor_base
        self.cor_passe_mouse = cor_passe_mouse
        self.texto_original = texto
        self.texto_render = self.fonte.render(self.texto_original, True, self.cor_base)
        self.texto_rect = self.texto_render.get_rect(center=(self.x_pos, self.y_pos))

    def atualizar(self, tela):
        tela.blit(self.texto_render, self.texto_rect)

    def verificar_entrada(self, posicao):
        return self.texto_rect.collidepoint(posicao)

    def mudar_cor(self, posicao):
        cor = self.cor_passe_mouse if self.texto_rect.collidepoint(posicao) else self.cor_base
        self.texto_render = self.fonte.render(self.texto_original, True, cor)
        self.texto_rect = self.texto_render.get_rect(center=(self.x_pos, self.y_pos))
