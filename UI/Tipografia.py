import pygame


class Tipografia:
    def __init__(self, pos:tuple[float, float], text:str, color):
        self.pos = pos
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(topleft=self.pos)
        surface.blit(text_surface, text_rect)