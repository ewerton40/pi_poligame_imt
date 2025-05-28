import pygame
import Constantes
from UI.Botao import Botao
from Telas.Tela import Tela

class TelaAcerto(Tela):
    def __init__(self, screen, transition_call):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.transition_call = transition_call
        self.font = pygame.font.Font(None, 32)
        self.texto_vitoria = "Parabéns!"
        self.texto_final = "Você alcançou 1.000.000 pontos!"
        
        # Carregar e redimensionar a imagem de fundo
        self.fundo_imagem = pygame.image.load("imagens/acerto.jpg")
        self.fundo_imagem = pygame.transform.scale(self.fundo_imagem, (Constantes.largura, Constantes.altura))

        # Botão de voltar ao início
        self.botao_voltar = Botao(
            (775, 650), (200, 50),
            pygame.Color("gray"), "Voltar ao Início",
            pygame.font.Font(None, 32)
        )

        self.pontuacao = 0
        self.incremento = 10000


    def load(self):
        self.is_loaded = True

    def draw(self):
        self.screen.blit(self.fundo_imagem, (0, 0))

        # Texto de vitória — ajustar posição aqui
        texto_vitoria_surface = self.font.render(self.texto_vitoria, True, pygame.Color("white"))
        self.screen.blit(texto_vitoria_surface, (900, 500))  # Mude (100, 150) para a posição desejada

        # Texto final — ajustar posição aqui
        texto_final_surface = self.font.render(self.texto_final, True, pygame.Color("white"))
        self.screen.blit(texto_final_surface, (780, 450))  # Mude (100, 250) para a posição desejada

        # Pontuação — ajustar posição aqui
        texto_pontos_surface = self.font.render(f"Pontos: {self.pontuacao}", True, pygame.Color("white"))
        self.screen.blit(texto_pontos_surface, (880, 400))  # Mude (100, 350) para a posição desejada

        # Botão
        self.botao_voltar.draw(self.screen)
        if self.botao_voltar.check_button():
            self.transition_call()

    def atualizar_pontuacao(self):
        if self.pontuacao < 1000000:
            self.pontuacao += self.incremento
        else:
            self.pontuacao = 1000000
