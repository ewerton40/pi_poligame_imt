import pygame
import Constantes

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor_fundo,fonte):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor_fundo = cor_fundo
        self.cor_sombra = Constantes.cor_rgb_sombra_botao
        self.cor_texto = Constantes.cor_rgb_texto_botao
        self.fonte = fonte

    def desenhar_botao(self, tela):
        pygame.draw.rect(tela, self.cor_sombra, self.rect.move(5, 5), border_radius=12)
       
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=12)
        texto_render = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        tela.blit(texto_render, texto_rect)    
    
    def foi_clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(evento.pos)     
    