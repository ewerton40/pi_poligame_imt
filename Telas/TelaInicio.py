import pygame
from pygame.locals import *
from sys import exit
import Constantes 
import Botao as Botao



class TelaInicio:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((Constantes.largura, Constantes.altura))
        pygame.display.set_caption(Constantes.titulo_jogo)
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        self.fonte_botao = pygame.font.SysFont(None, 40)
        self.botao_jogar = Botao.Botao("Jogar", 540, 400, 150, 50, (4, 180, 196), self.fonte_botao)
        


    def jogar(self):
        self.jogando = True
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit
                    exit()

            self.tela.blit(self.imagem_fundo, (0, 0))  
            self.tela.blit(self.imagem_logo, (400, 100))
            self.botao_jogar.desenhar_botao(self.tela)
            pygame.display.update()
            self.relogio.tick(60)
            
        
    def logo(self):
        self.imagem_logo = pygame.image.load('imagens/logo_pi.png').convert()

    def fundo_login(self):
        self.imagem_fundo = pygame.image.load('imagens/fundo_pi.jpeg').convert()
    
g = TelaInicio()

while g.esta_rodando:
    g.logo()
    g.fundo_login()
    g.jogar() 




