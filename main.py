# main.py

import pygame
import sys
import Constantes  # Certifique-se de que esse módulo exista
from Botao import Botao            # Certifique-se de que esse módulo exista

# Aqui você pode copiar sua classe TelaLogin completa (que você já enviou), ou importá-la de outro arquivo:
from Telas.TelaLogin import TelaLogin  # Se você tiver separado a classe em TelaLogin.py

def quit_game():
    pygame.quit()
    sys.exit()

def transition(tela):
    print("Transição de tela:", type(tela))

def main():
    pygame.init()
    screen = pygame.display.set_mode((Constantes.largura, Constantes.altura))
    pygame.display.set_caption("Teste Tela de Login")
    clock = pygame.time.Clock()

    tela_login = TelaLogin(screen, transition, quit_game)
    tela_login.load()

    while True:
        tela_login.run()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()