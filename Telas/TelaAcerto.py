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
        self.font = pygame.font.Font(None, 32)
        self.texto_vitoria = "Parabéns!"
        self.texto_final = "Você ganhou 1.000.000 de reais!"
        
        # Carregar e redimensionar a imagem de fundo
        self.fundo_imagem = pygame.image.load("imagens/acerto.jpg")
        self.fundo_imagem = pygame.transform.scale(self.fundo_imagem, (Constantes.largura, Constantes.altura))

        # Botão de voltar ao início
        self.botao_voltar = Botao(
            (860, 650), (200, 50),
            pygame.Color("skyblue"), "Voltar ao Início",
            pygame.font.Font(None, 32)
        )



    def load(self):
        self.is_loaded = True

    def run(self, events):
        self.screen.blit(self.fundo_imagem, (0, 0))

        # Texto de vitória — ajustar posição aqui
        texto_vitoria_surface = self.font.render(self.texto_vitoria, True, pygame.Color("blue"))
        self.screen.blit(texto_vitoria_surface, (900, 500))  # Mude (100, 150) para a posição desejada

        # Texto final — ajustar posição aqui
        texto_final_surface = self.font.render(self.texto_final, True, pygame.Color("blue"))
        self.screen.blit(texto_final_surface, (780, 450))  # Mude (100, 250) para a posição desejada

        # Botão
        self.botao_voltar.draw(self.screen)
        if self.botao_voltar.check_button():
            from Telas.TelaInicio import TelaInicio
            self.transition_call((TelaInicio(self.screen, self.transition_call, self.quit_game)))

    def atualizar_pontuacao(self):
        if self.pontuacao < 1000000:
            self.pontuacao += self.incremento
        else:
            self.pontuacao = 1000000

    
