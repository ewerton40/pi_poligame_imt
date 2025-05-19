import pygame

pygame.init()
pygame.font.init()


from addPerguntaTela import abrir_nova_janela
from rankingAlunos import abrir_janela2
from adicionarAluno import abrir_tela_adicionar_aluno
from Classes.elementos_visuais import Cores, Fonte, desenhar_texto_centralizado
from Classes.botao import Botao
from Classes.item_lista import ItemLista
from Classes.gerenciador_perguntas import GerenciadorPerguntas
from Classes.componentes import criar_caixa_texto, desenhar_caixa_texto, criar_botao, desenhar_botao
from Classes.tela_gerenciamento import TelaGerenciamento


if __name__ == '__main__':
    tela_gerenciamento = TelaGerenciamento()
    tela_gerenciamento.executar()