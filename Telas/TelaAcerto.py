import pygame
import Constantes
from UI.Botao import Botao
from Telas.Tela import Tela

class TelaAcerto(Tela):
    def __init__(self, screen, transition_call, quit_game, id_aluno):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.transition_call = transition_call
        self.quit_game = quit_game
        self.id_aluno = id_aluno

        self.fundo_imagem = pygame.image.load("imagens/ganhar.png")
        self.fundo_imagem = pygame.transform.scale(self.fundo_imagem, (Constantes.largura, Constantes.altura))

        self.botao_voltar = Botao(
            (885, 650), (230, 50),
            pygame.Color("skyblue"), "Voltar ao Início",
            pygame.font.Font(None, 32)
        )

        # Fade + movimento
        self.alpha = 0
        self.alpha_speed = 3


    def load(self):
        self.is_loaded = True

    def run(self, events):
        self.screen.blit(self.fundo_imagem, (0, 0))

        # Botão
        self.botao_voltar.draw(self.screen)
        if self.botao_voltar.check_button():
            from Telas.TelaInicio import TelaInicio
            self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game, user_data={"tipo": "Aluno", "id": self.id_aluno}))
