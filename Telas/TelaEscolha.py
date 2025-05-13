import pygame
# from .TelaAdmin import TelaAdmin
from Telas.Tela import Tela
import sys
from sys import exit
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Telas.TelaAdmin import TelaAdmin
from Botao import Botao




class TelaEscolha(Tela):
    def __init__(self, screen, transition_call):
         super().__init__(screen, transition_call)
         self.screen = screen
         self.pos = 0
         self.images = {}
         fonte = pygame.font.SysFont("Arial", 24) 
         self.portugues = Botao((325, 170), (170, 90), pygame.Color("skyblue"), "Português", fonte)
         self.quimica = Botao((325, 320), (170, 90), pygame.Color("skyblue"), "Química", fonte)


    def load(self):
        self.pos = 0

        self.images = {
            "background": pygame.image.load("imagens/fundo_pi.jpeg").convert()
        }

        self.is_loaded = all(image is not None for image in self.images.values())


    
    def run(self):
        if self.is_loaded:
            self.screen.fill("black")
            self.screen.blit(self.images["background"], (self.pos, 0))

    
        self.portugues.draw(self.screen)
        if self.portugues.check_button():
            self.transition_call(TelaAdmin(self.screen, self.transition_call))

        self.quimica.draw(self.screen)
        if self.quimica.check_button():   
            self.transition_call(TelaAdmin(self.screen, self.transition_call))          