# Arquivo: Classes/componentes.py
import pygame
from .elementos_visuais import Cores, Fonte, desenhar_texto_centralizado,  escalar, escalar_y



def criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
    rect = pygame.Rect(x, y, largura, altura)
    texto = texto_inicial
    label = texto_label
    ativo = False
    return {"rect": rect, "texto": texto, "label": label, "ativo": ativo}

def desenhar_caixa_texto(tela, caixa):
    texto_renderizado = Fonte.PADRAO.render(caixa["texto"], True, Cores.TEXTO) # <--- Acesso a Fonte.PADRAO ANTES da inicialização explícita
    cor_borda = Cores.BORDA_CAIXA_TEXTO_ATIVO if caixa["ativo"] else Cores.BORDA_CAIXA_TEXTO_INATIVO
    pygame.draw.rect(tela, Cores.CAIXA_TEXTO_FUNDO, caixa["rect"], 0, border_radius=10)
    pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=10)
    texto_renderizado = Fonte.PADRAO.render(caixa["texto"], True, Cores.TEXTO)
    tela.blit(texto_renderizado, (caixa["rect"].x + 10, caixa["rect"].y + (caixa["rect"].height - texto_renderizado.get_height()) // 2))
    texto_label_renderizado = Fonte.PEQUENA.render(caixa["label"], True, Cores.TEXTO)
    tela.blit(texto_label_renderizado, (caixa["rect"].x + 10, caixa["rect"].y - texto_label_renderizado.get_height() - 5))
    texto_renderizado = Fonte.get_PADRAO().render(caixa["texto"], True, Cores.TEXTO) 

def criar_botao(texto, x, y, largura, altura):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto}

def desenhar_botao(tela, botao):
    pygame.draw.rect(tela, Cores.BOTOES_MENU, botao["rect"], 0, border_radius=10)
    desenhar_texto_centralizado(tela, botao["texto"], Fonte.PEQUENA, Cores.TEXTO_BOTAO, botao["rect"])
    return botao["rect"]

class Botao:
    def __init__(self, rect, texto, font, hover_color=Cores.BUTTON_HOVER, normal_color=Cores.BUTTON_COLOR, text_color=Cores.WHITE):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.font = font
        self.hover_color = hover_color
        self.normal_color = normal_color
        self.text_color = text_color
        self.is_hovering = False
        self.texto_renderizado = self.font.render(self.texto, True, self.text_color) # Usa a 'font' passada, que PODE ser Fonte.PADRAO


    def desenhar(self, surface):
        color = self.hover_color if self.is_hovering else self.normal_color
        pygame.draw.rect(surface, Cores.BLACK, self.rect)
        inner_rect = self.rect.inflate(-escalar(16, 1920, surface.get_width()), -escalar_y(16, 1080, surface.get_height()))
        pygame.draw.rect(surface, color, inner_rect)
        text_surf = self.font.render(self.texto, True, self.text_color)
        text_rect = text_surf.get_rect(center=inner_rect.center)
        surface.blit(text_surf, text_rect)

    def verificar_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def verificar_clique(self, event):
        return self.is_hovering and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
    
class Alternativa:
    def __init__(self, rect, texto, font, selecionada_color=Cores.SELECTED_COLOR, hover_color=Cores.BUTTON_HOVER, normal_color=Cores.WHITE, text_color=Cores.BLACK):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.font = font
        self.selecionada_color = selecionada_color
        self.hover_color = hover_color
        self.normal_color = normal_color
        self.text_color = text_color
        self.selecionada = False
        self.is_hovering = False

    def desenhar(self, surface):
        color = self.selecionada_color if self.selecionada else (self.hover_color if self.is_hovering else self.normal_color)
        pygame.draw.rect(surface, Cores.BLACK, self.rect)
        inner_rect = self.rect.inflate(-escalar(16, 1920, surface.get_width()), -escalar_y(16, 1080, surface.get_height()))
        pygame.draw.rect(surface, color, inner_rect)
        text_surf = self.font.render(f"{self.texto}", True, self.text_color)
        text_rect = text_surf.get_rect(midleft=(inner_rect.x + escalar(10, 1920, surface.get_width()), inner_rect.centery))
        surface.blit(text_surf, text_rect)

    def verificar_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)

    def verificar_clique(self, event):
        return self.is_hovering and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1