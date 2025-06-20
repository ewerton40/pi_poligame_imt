import pygame

#Classe contendo características gerais da pontuação de dentro do jogo.
class Pontuacao:
    def __init__(self, pos:tuple[float, float], size:tuple[float, float], color):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color = color
        self.score = 0
        self.score_incrementer = 100000
        self.border_color = pygame.Color("white")
        self.font = pygame.font.SysFont("Arial", 32)

#Definindo a interface da pontuação.
    def draw(self, surface):
        border_color = pygame.Color("black")
        border_width = 4
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, border_width)
        score_surface = self.font.render(str(self.score), True, pygame.Color("white"))
        score_rect = score_surface.get_rect(center=self.rect.center)
        surface.blit(score_surface, score_rect)

#Incrementando a pontuação.
    def increment_score(self):
        self.score = str(int(self.score) + self.score_incrementer)