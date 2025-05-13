import pygame
# from .TelaAdmin import TelaAdmin
from Telas.Tela import Tela
import sys
from sys import exit
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Constantes 
from Botao import Botao

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

class TelaInicio(Tela):
    def __init__(self, screen, transition_call, quit_game):
        super().__init__(screen, transition_call)
        self.quit = quit_game
        self.screen = screen
        self.pos = 0
        self.images = {}
        fonte = pygame.font.SysFont("Arial", 24)
        self.sair = Botao((325, 380), (150, 50), pygame.Color("gray"), "Sair", fonte)
        self.ranking = Botao((325, 420), (150, 50), pygame.Color("gray"), "Ranking", fonte)
        self.jogar = Botao((325, 300), (150, 50), pygame.Color("gray"), "Jogar", fonte)
        self.logo: pygame.Surface
       
        
    def load(self):
        self.pos = 0

        self.images = {
            "background": pygame.image.load("imagens/fundo_pi.jpeg").convert(),
            "logo": pygame.image.load("imagens/logo_pi.png").convert_alpha(),  
        }

        self.is_loaded = all(image is not None for image in self.images.values())

    def run(self):
        if self.is_loaded:
            self.screen.fill("black")
            self.screen.blit(self.images["background"], (self.pos, 0))
            self.screen.blit(self.images["logo"], ((Constantes.largura / 2 - self.images["logo"].get_width()
                                        // 2), 70)) #Posiciona o logo no centro da tela
           

            self.jogar.draw(self.screen)
            if self.jogar.check_button():
                self.transition_call(TelaAdmin(self.screen, self.transition_call)) #Se o botão jogar for pressionado, muda para a tela de jogo

           

            self.sair.draw(self.screen)
            if self.sair.check_button():
                self.quit() #Se o botão sair for pressionado, fecha o jogo


            if abs(self.pos) > Constantes.largura:
                self.pos = 0



# def quit_game():
#     pygame.quit()
#     sys.exit()

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption("Tela de Início")
#     clock = pygame.time.Clock()

#     tela_inicio = TelaInicio(screen, lambda x: print("Transição!"), quit_game)
#     tela_inicio.load()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quit_game()

#         tela_inicio.run()
#         pygame.display.update()
#         clock.tick(60)













#     def jogar(self):
#         self.jogando = True
#         while True:
#             for event in pygame.event.get():
#                 if event.type == QUIT:
#                     pygame.quit
#                     exit()

#             self.tela.blit(self.imagem_fundo, (0, 0))  
#             self.tela.blit(self.imagem_logo, (400, 100))
#             self.botao_jogar.desenhar_botao(self.tela)
#             pygame.display.update()
#             self.relogio.tick(60)
            
        
#     def logo(self):
#         self.imagem_logo = pygame.image.load('imagens/logo_pi.png').convert()

#     def fundo_login(self):
#         self.imagem_fundo = pygame.image.load('imagens/fundo_pi.jpeg').convert()
    
# g = TelaInicio()

# while g.esta_rodando:
#     g.logo()
#     g.fundo_login()
#     g.jogar() 




