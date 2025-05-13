import pygame


# Mock simples para teste (apenas para evitar erro)
class TelaAdmin:
    def __init__(self, screen, transition_call):
        self.screen = screen
        self.transition_call = transition_call
    
    def run(self):
        self.screen.fill((255, 0, 0))  # Tela vermelha só para teste
        fonte = pygame.font.SysFont("Arial", 36)
        texto = fonte.render("Tela Admin", True, (255, 255, 255))
        self.screen.blit(texto, (200, 200))

        