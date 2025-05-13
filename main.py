# main.py
import pygame
from Telas.TelaInicio import TelaInicio

def quit_game():
    pygame.quit()
    exit()

def transition(tela):
    print("Transição de tela:", type(tela))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Poligame")
    clock = pygame.time.Clock()

    tela_inicio = TelaInicio(screen, transition, quit_game)
    tela_inicio.load()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        tela_inicio.run()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
