import pygame

# Função principal que inicializa Pygame antes de importar módulos que usam fontes

def main():
    pygame.init()
    pygame.font.init()

    # Importações adiadas após inicialização de Pygame/fontes
    from TelaAddPergunta import AddPerguntaTela
    from RankingAlunos import JanelaRanking
    from TelaAddAluno import TelaAdicionarAluno
    from TelaGerenciamento import TelaGerenciamento


    from Classes.botao import Botao
    from Classes.item_lista import ItemLista
    from Classes.gerenciador_perguntas import GerenciadorPerguntas
    from Classes.componentes import UIComponentes

    # Cria e executa a tela de gerenciamento
    tela_gerenciamento = TelaGerenciamento()
    tela_gerenciamento.executar()

    pygame.quit()

if __name__ == '__main__':
    main()
