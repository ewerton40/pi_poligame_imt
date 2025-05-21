import pygame
import Constantes
from Botao import Botao
import pickle
from Telas.TelaInicio import TelaInicio

class TelaErro:
    def __init__(self, screen, transition_call):
        self.screen = screen
        self.transition_call = transition_call
        self.font = pygame.font.Font(None, 28)
        self.texto_erro = "Você errou a pergunta!"
        self.texto_informacao = "Você perdeu os pontos e voltou ao último checkpoint!"

        self.fundo_imagem = pygame.image.load("imagens/erro.jpg")
        self.fundo_imagem = pygame.transform.scale(
            self.fundo_imagem, (Constantes.largura, Constantes.altura)
        )

        fonte_botao = pygame.font.Font(None, 28)

        # Apenas o botão "Voltar ao Início"
        self.botao_inicio = Botao(
            (875, 650), (200, 45), pygame.Color("gray"),
            "Voltar ao Início", fonte_botao
        )

        self.pontuacao = 0
        self.checkpoint = 0
        self.incremento = 10000
        self.checkpoints = [i * 20000 for i in range(1, 51)]

    def desenhar_erro(self):
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

        if self.botao_inicio.check_button():
            self.transition_call(TelaInicio(self.screen, self.transition_call, pygame.quit))

    def atualizar_pontuacao(self, resposta_correta: bool):
        if resposta_correta:
            self.pontuacao += self.incremento
            if self.pontuacao >= self.checkpoints[self.checkpoint]:
                self.checkpoint += 1
        else:
            self.pontuacao = self.checkpoints[self.checkpoint - 1] if self.checkpoint > 0 else 0

    def salvar_pontuacao(self):
        with open("pontos_salvos.pkl", "wb") as file:
            pickle.dump(self.pontuacao, file)

    def exibir_tela_erro(self):
        rodando_erro = True
        while rodando_erro:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando_erro = False
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    if self.botao_inicio.rect.collidepoint(pos_mouse):
                        rodando_erro = False
                        self.transition_call(TelaInicio(self.screen, self.transition_call, pygame.quit))
                        return False

            self.screen.fill(pygame.Color("black"))
            self.desenhar_erro()
            pygame.display.flip()
        return True
