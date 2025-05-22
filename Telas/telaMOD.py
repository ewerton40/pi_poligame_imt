import pygame

# Função principal que inicializa Pygame antes de importar módulos que usam fontes

def main():
    pygame.init()
    pygame.font.init()

    # Importações adiadas após inicialização de Pygame/fontes
    from addPerguntaTela import abrir_nova_janela
    from rankingAlunos import abrir_janela2
    from adicionarAluno import abrir_tela_adicionar_aluno
    from Classes.botao import Botao
    from Classes.item_lista import ItemLista
    from Classes.gerenciador_perguntas import GerenciadorPerguntas
    from Classes.componentes import criar_caixa_texto, desenhar_caixa_texto, criar_botao, desenhar_botao
    from Classes.tela_gerenciamento import TelaGerenciamento

    # Cria e executa a tela de gerenciamento
    tela_gerenciamento = TelaGerenciamento()
    tela_gerenciamento.executar()

    pygame.quit()

if __name__ == '__main__':
    main()
