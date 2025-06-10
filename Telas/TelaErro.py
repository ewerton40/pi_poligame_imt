import pygame
import Constantes
from UI.Botao import Botao
from Telas.Tela import Tela
from Telas.TelaInicio import TelaInicio

class TelaErro(Tela):
    def __init__(self, screen, transition_call, pontuacao_visual, quit_game, id_aluno):
        super().__init__(screen, transition_call)
        self.screen = screen        
        self.transition_call = transition_call
        self.quit_game = quit_game
        self.id_aluno = id_aluno
        self.font = pygame.font.Font(None, 28)
        self.texto_erro = "Você errou a pergunta!"
        self.texto_informacao = "Você perdeu e voltou ao último checkpoint!"
        self.pontuacao = pontuacao_visual
        self.fundo_imagem = pygame.image.load("imagens/erro.jpg")
        self.fundo_imagem = pygame.transform.scale(
            self.fundo_imagem, (Constantes.largura, Constantes.altura)
        )

        fonte_botao = pygame.font.Font(None, 28)

        
        self.botao_inicio = Botao((860, 650), (200, 45), pygame.Color("skyblue"), "Voltar ao Início", fonte_botao  )

    def load(self):
        self.is_loaded = True  

    def run(self, events):
        self.screen.blit(self.fundo_imagem, (0, 0))

        texto_erro_surface = self.font.render(self.texto_erro, True, pygame.Color("red"))
        texto_informacao_surface = self.font.render(self.texto_informacao, True, pygame.Color("red"))
        texto_erro_rect = texto_erro_surface.get_rect(center=(950, 450))
        texto_informacao_rect = texto_informacao_surface.get_rect(center=(950, 500))
        self.screen.blit(texto_erro_surface, texto_erro_rect)
        self.screen.blit(texto_informacao_surface, texto_informacao_rect)

        texto_pontuacao = f"Premiação: R${self.pontuacao}"
        texto_pontuacao_surface = self.font.render(texto_pontuacao, True, pygame.Color("black"))
        texto_pontuacao_rect = texto_pontuacao_surface.get_rect(center=(950, 550))
        self.screen.blit(texto_pontuacao_surface, texto_pontuacao_rect)

        self.botao_inicio.draw(self.screen)
        if self.botao_inicio.check_button():
            from Telas.TelaInicio import TelaInicio
            self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game, user_data={"tipo": "Aluno", "id": self.id_aluno}))

    

