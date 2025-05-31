import pygame
import Constantes
from UI.Botao import Botao
from Telas.Tela import Tela

class TelaAcerto(Tela):
    def __init__(self, screen, transition_call, quit_game):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.transition_call = transition_call
        self.quit_game = quit_game
        self.font_grande = pygame.font.Font(None, 80)
        self.font_media = pygame.font.Font(None, 40)

        self.texto_vitoria = "Parabéns!"
        self.texto_final = "Você ganhou 1.000.000 de reais!"

        self.fundo_imagem = pygame.image.load("imagens/acerto.jpg")
        self.fundo_imagem = pygame.transform.scale(self.fundo_imagem, (Constantes.largura, Constantes.altura))

        self.botao_voltar = Botao(
            (860, 650), (200, 50),
            pygame.Color("skyblue"), "Voltar ao Início",
            pygame.font.Font(None, 32)
        )

        # Fade + movimento
        self.alpha = 0
        self.alpha_speed = 3

        self.texto1_y = 580  # começa abaixo da posição final (500)
        self.texto2_y = 530  # começa abaixo da posição final (450)
        self.target_texto1_y = 500
        self.target_texto2_y = 450

    def load(self):
        self.is_loaded = True

    def run(self, events):
        self.screen.blit(self.fundo_imagem, (0, 0))

        # Renderizar superfícies
        texto1_surface = self.font_grande.render(self.texto_vitoria, True, pygame.Color("blue"))
        texto2_surface = self.font_media.render(self.texto_final, True, pygame.Color("blue"))

        texto1_surface.set_alpha(self.alpha)
        texto2_surface.set_alpha(self.alpha)

        # Desenhar com movimento e fade
        self.screen.blit(texto2_surface, (740, self.texto2_y))
        self.screen.blit(texto1_surface, (835, self.texto1_y))

        # Atualizar alpha
        if self.alpha < 255:
            self.alpha += self.alpha_speed

        # Atualizar posição suavemente
        if self.texto1_y > self.target_texto1_y:
            self.texto1_y -= 0.5
        if self.texto2_y > self.target_texto2_y:
            self.texto2_y -= 0.5

        # Botão
        self.botao_voltar.draw(self.screen)
        if self.botao_voltar.check_button():
            from Telas.TelaInicio import TelaInicio
            self.transition_call((TelaInicio(self.screen, self.transition_call, self.quit_game)))
