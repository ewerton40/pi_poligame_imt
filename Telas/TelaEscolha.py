import pygame
from Telas.Tela import Tela
import sys
from sys import exit
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Telas.TelaPergunta import TelaPergunta
from UI.Botao import Botao
from util import DATABASE




class TelaEscolha(Tela):
    def __init__(self, screen, transition_call,  quit_game, id_aluno):
         super().__init__(screen, transition_call)
         self.screen = screen
         self.images = {}
         self.quit_game = quit_game
         self.id_aluno = id_aluno
         self.id_materia = None
         fonte = pygame.font.SysFont("Arial", 24) 
         self.portugues = Botao((580, 180), (170, 90), pygame.Color("skyblue"), "Português", fonte)
         self.quimica = Botao((580, 340), (170, 90), pygame.Color("skyblue"), "Química", fonte)
         self.voltar = Botao((20,20), (100, 60), pygame.Color("skyblue"), "Voltar", fonte)


    def load(self):
        self.pos = 0
        self.images = {
            "background": pygame.image.load("imagens/fundo_pi.jpeg").convert()
        }

        self.is_loaded = all(image is not None for image in self.images.values())


    
    def run(self, events):
        if self.is_loaded:
            self.screen.fill("black")
            self.screen.blit(self.images["background"], (self.pos, 0))

        
        self.voltar.draw(self.screen)
        if self.voltar.check_button():
            from Telas.TelaInicio import TelaInicio
            self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game))

        self.portugues.draw(self.screen)
        if self.portugues.check_button():
            self.id_materia = 1 
            id_partida = DATABASE.criar_partida(self.id_aluno, self.id_materia)
            self.transition_call(TelaPergunta(self.screen, self.transition_call, self.id_materia, self.quit_game, id_partida=id_partida))

        self.quimica.draw(self.screen)
        if self.quimica.check_button():
            self.id_materia = 2
            id_partida = DATABASE.criar_partida(self.id_aluno, self.id_materia)   
            self.transition_call(TelaPergunta(self.screen, self.transition_call, self.id_materia, self.quit_game, id_partida=id_partida))          