# import pygame
# import Constantes
# from Botao import Botao

# class TelaAcerto:
#     def __init__(self, screen, transition_call):  # Corrigido de _init para _init_
#         self.screen = screen
#         self.transition_call = transition_call
#         self.font = pygame.font.Font(None, 28)  # Fonte maior para o título e pontuação final
#         self.texto_vitoria = "Parabéns!"
#         self.texto_final = "Você alcançou 1.000.000 pontos!"
        
#         # Carregar a imagem de fundo
#         self.fundo_imagem = pygame.image.load("imagens/acerto.jpg")  # Caminho da imagem JPEG
#         self.fundo_imagem = pygame.transform.scale(self.fundo_imagem, (Constantes.largura, Constantes.altura))  # Ajusta a imagem para o tamanho da tela

#         # Botão para voltar à tela inicial
#         self.botao_voltar = Botao((775, 650), (200, 50), pygame.Color("gray"), "Voltar ao Início", pygame.font.Font(None, 32))
#         self.pontuacao = 0
#         self.incremento = 10000  # Incrementa 1000 pontos por segundo

#     def draw(self):
#         # Preencher a tela com a imagem de fundo
#         self.screen.blit(self.fundo_imagem, (0, 0))

#         # Renderizar os textos
#         texto_vitoria_surface = self.font.render(self.texto_vitoria, True, pygame.Color("white"))
#         texto_final_surface = self.font.render(self.texto_final, True, pygame.Color("white"))

#         # Obter os retângulos para centralizar os textos
#         texto_vitoria_rect = texto_vitoria_surface.get_rect(center=(Constantes.largura // 2, 150))
#         texto_final_rect = texto_final_surface.get_rect(center=(Constantes.largura // 2, 250))

#         # Desenhar os textos na tela
#         self.screen.blit(texto_vitoria_surface, texto_vitoria_rect)
#         self.screen.blit(texto_final_surface, texto_final_rect)

#         # Exibir a pontuação na tela
#         texto_pontos_surface = self.font.render(f"Pontos: {self.pontuacao}", True, pygame.Color("white"))
#         texto_pontos_rect = texto_pontos_surface.get_rect(center=(Constantes.largura // 2, 350))
#         self.screen.blit(texto_pontos_surface, texto_pontos_rect)

#         # Desenhar o botão de voltar
#         self.botao_voltar.draw(self.screen)
#         if self.botao_voltar.check_button():
#             self.transition_call()  # Chama a função para voltar à tela inicial

#     def atualizar_pontuacao(self):
#         # Aumenta a pontuação até 1 milhão
#         if self.pontuacao < 1000000:
#             self.pontuacao += self.incremento
#         else:
#             self.pontuacao = 1000000  # Garante que o máximo será 1 milhão

import pygame
import Constantes
from UI.Botao import Botao

class TelaAcerto:
    def __init__(self, screen, transition_call):
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
