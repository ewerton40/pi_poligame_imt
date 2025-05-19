# Arquivo: Classes/botao.py
import pygame
from .elementos_visuais import Fonte

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor, cor_texto, funcao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.funcao = funcao
        self.texto_renderizado = Fonte.PADRAO.render(texto, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(center=self.rect.center)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=5)
        tela.blit(self.texto_renderizado, self.texto_rect)

    def verificar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)