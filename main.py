# main.py
import pygame
from Telas.TelaInicio import TelaInicio
from Telas.TelaEscolha import TelaEscolha
import Constantes
from sys import exit


def quit_game():
    pygame.quit()
    exit()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(Constantes.titulo_jogo)
    clock = pygame.time.Clock()

    tela_atual = [None]  # Lista com referência mutável

    # Define função de transição
    def transition(nova_tela):
        print("Transição de tela:", type(nova_tela))
        tela_atual[0] = nova_tela
        tela_atual[0].load()

    # Inicializa a primeira tela com a função de transição
    tela_atual[0] = TelaInicio(screen, transition, quit_game)
    tela_atual[0].load()

    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        tela_atual[0].run()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()





















# def quit_game():
#     pygame.quit()
#     exit()

# def transition(tela):
#     print("Transição de tela:", type(tela))

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption(Constantes.titulo_jogo)
#     clock = pygame.time.Clock()

#     tela_atual = TelaInicio(screen, transition, quit_game)
#     tela_atual.load()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 quit_game()

#         tela_atual.run()
#         pygame.display.update()
#         clock.tick(60)

# if __name__ == "__main__":
#     main()
