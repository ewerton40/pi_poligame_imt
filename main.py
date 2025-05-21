# telaErro

import pygame
from Telas.TelaErro import TelaErro
import Botao
import Constantes

def transition_function():
    print("Voltando ao jogo!")

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((Constantes.largura, Constantes.altura))
    pygame.display.set_caption("Show do Milhão")
    tela_erro = TelaErro(screen, transition_function)
    resposta_correta = False  # Simulando uma resposta errada
    tela_erro.atualizar_pontuacao(resposta_correta)
    tela_erro.exibir_tela_erro()
    tela_erro.salvar_pontuacao()
    pygame.quit()

if __name__ == "__main__":
    run_game()




# #acerto
# # main.py
# import pygame
# from Telas.TelaAcerto import TelaAcerto
# import Constantes

# def transition_function():
#     print("Voltando à tela inicial!")

# pygame.init()
# screen = pygame.display.set_mode((Constantes.largura, Constantes.altura))
# pygame.display.set_caption("Tela de Acerto")

# tela_acerto = TelaAcerto(screen, transition_function)

# running = True
# clock = pygame.time.Clock()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     tela_acerto.atualizar_pontuacao()
#     tela_acerto.draw()

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()









# main.py

# import pygame
# import sys
# import Constantes  # Certifique-se de que esse módulo exista
# from Botao import Botao            # Certifique-se de que esse módulo exista

# # Aqui você pode copiar sua classe TelaLogin completa (que você já enviou), ou importá-la de outro arquivo:
# from Telas.TelaLogin import TelaLogin  # Se você tiver separado a classe em TelaLogin.py

# def quit_game():
#     pygame.quit()
#     sys.exit()

# def transition(tela):
#     print("Transição de tela:", type(tela))

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((Constantes.largura, Constantes.altura))
#     pygame.display.set_caption("Teste Tela de Login")
#     clock = pygame.time.Clock()

#     tela_login = TelaLogin(screen, transition, quit_game)
#     tela_login.load()

#     while True:
#         tela_login.run()
#         pygame.display.update()
#         clock.tick(60)

# if __name__ == "__main__":
#     main()