import pygame

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor, cor_texto, funcao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.funcao = funcao
        # Renderiza texto diretamente com fonte embutida
        fonte = pygame.font.Font(None, 30)
        self.texto_renderizado = fonte.render(texto, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(center=self.rect.center)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=5)
        tela.blit(self.texto_renderizado, self.texto_rect)

    def verificar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
