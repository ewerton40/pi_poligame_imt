import pygame
from Telas.Tela import Tela
import sys
from sys import exit
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Constantes 
from UI.Botao import Botao 
from Telas.TelaEscolha import TelaEscolha

class TelaInicio(Tela):
    def __init__(self, screen, transition_call, quit_game):
        super().__init__(screen, transition_call)
        self.quit = quit_game
        self.screen = screen
        self.pos = 0
        self.images = {}
        fonte = pygame.font.SysFont("Arial", 24)
        self.sair = Botao((580, 470), (150, 50), pygame.Color("gray"), "Sair", fonte)
        self.jogar = Botao((580, 400), (150, 50), pygame.Color("gray"), "Jogar", fonte)
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
                self.transition_call(TelaEscolha(self.screen, self.transition_call)) #Se o botão jogar for pressionado, muda para a tela de jogo

           

            self.sair.draw(self.screen)
            if self.sair.check_button():
                self.quit() #Se o botão sair for pressionado, fecha o jogo


            if abs(self.pos) > Constantes.largura:
                self.pos = 0


