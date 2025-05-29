import pygame
import Constantes
from UI.Botao import Botao
from Telas.Tela import Tela
from Telas.TelaInicio import TelaInicio

class TelaErro(Tela):
    def __init__(self, screen, transition_call, checkpoint, quit_game):
        super().__init__(screen, transition_call)
        self.screen = screen        
        self.transition_call = transition_call
        self.quit_game = quit_game
        self.font = pygame.font.Font(None, 28)
        self.texto_erro = "Você errou a pergunta!"
        self.texto_informacao = "Você perdeu os pontos e voltou ao último checkpoint!"
        self.pontuacao = checkpoint
        self.fundo_imagem = pygame.image.load("imagens/erro.jpg")
        self.fundo_imagem = pygame.transform.scale(
            self.fundo_imagem, (Constantes.largura, Constantes.altura)
        )

        fonte_botao = pygame.font.Font(None, 28)

        # Apenas o botão "Voltar ao Início"
        self.botao_inicio = Botao((875, 650), (200, 45), pygame.Color("skyblue"), "Voltar ao Início", fonte_botao  )

    def load(self):
        # Se quiser carregar outras imagens, faça aqui
        self.is_loaded = True  # indica que carregou corretamente

    def run(self, events):
        self.screen.blit(self.fundo_imagem, (0, 0))

        texto_erro_surface = self.font.render(self.texto_erro, True, pygame.Color("red"))
        texto_informacao_surface = self.font.render(self.texto_informacao, True, pygame.Color("red"))
        texto_erro_rect = texto_erro_surface.get_rect(center=(950, 450))
        texto_informacao_rect = texto_informacao_surface.get_rect(center=(950, 500))
        self.screen.blit(texto_erro_surface, texto_erro_rect)
        self.screen.blit(texto_informacao_surface, texto_informacao_rect)

        texto_pontuacao = f"Pontuação: {self.pontuacao}"
        texto_pontuacao_surface = self.font.render(texto_pontuacao, True, pygame.Color("white"))
        texto_pontuacao_rect = texto_pontuacao_surface.get_rect(center=(950, 550))
        self.screen.blit(texto_pontuacao_surface, texto_pontuacao_rect)

        self.botao_inicio.draw(self.screen)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_inicio.rect.collidepoint(event.pos):
                    # Volta para tela inicial
                    self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game))

