# Arquivo: Classes/item_lista.py
import pygame
from .elementos_visuais import Cores, Fonte
from .botao import Botao

class ItemLista:
    ALTURA = 50
    MARGEM = 10
    LARGURA_BOTAO_FILTRO = 80
    ALTURA_BOTAO_FILTRO = 30
    ESPACAMENTO_FILTRO = 30
    LARGURA_BOTAO_EDITAR = 80

    def __init__(self, texto_pergunta, y, largura_total):
        self.largura_total = largura_total
        self.y = y
        self.x_item = self.MARGEM
        self.largura_item = largura_total - 2 * self.MARGEM
        self.rect = pygame.Rect(self.x_item, y, self.largura_item, self.ALTURA)
        self.texto_renderizado = Fonte.PADRAO.render(texto_pergunta, True, Cores.TEXTO_LISTA)
        self.texto_rect = self.texto_renderizado.get_rect(midleft=(self.x_item + self.MARGEM, y + self.ALTURA // 2))
        self.botoes_filtro = self._criar_botoes_filtro()
        self.botao_editar = self._criar_botao_editar()
        self.botoes_rects = [botao.rect for botao in self.botoes_filtro] + [self.botao_editar.rect]

    def _criar_botoes_filtro(self):
        x_filtro1 = self.x_item + self.largura_item - 3 * self.LARGURA_BOTAO_FILTRO - 2 * self.ESPACAMENTO_FILTRO - self.MARGEM
        x_filtro2 = self.x_item + self.largura_item - 2 * self.LARGURA_BOTAO_FILTRO - self.ESPACAMENTO_FILTRO - self.MARGEM
        x_filtro3 = self.x_item + self.largura_item - self.LARGURA_BOTAO_FILTRO - self.MARGEM
        y_botao = self.y + (self.ALTURA - self.ALTURA_BOTAO_FILTRO) // 2
        botao1 = Botao("Filtro()", x_filtro1, y_botao, self.LARGURA_BOTAO_FILTRO, self.ALTURA_BOTAO_FILTRO, Cores.BOTAO_FILTRO, Cores.TEXTO_BOTOES, "filtrar")
        botao2 = Botao("Filtro()", x_filtro2, y_botao, self.LARGURA_BOTAO_FILTRO, self.ALTURA_BOTAO_FILTRO, Cores.BOTAO_FILTRO, Cores.TEXTO_BOTOES, "filtrar")
        botao3 = Botao("Filtro()", x_filtro3, y_botao, self.LARGURA_BOTAO_FILTRO, self.ALTURA_BOTAO_FILTRO, Cores.BOTAO_FILTRO, Cores.TEXTO_BOTOES, "filtrar")
        return [botao1, botao2, botao3]

    def _criar_botao_editar(self):
        x_editar = self.x_item + self.largura_item - self.LARGURA_BOTAO_EDITAR - self.MARGEM
        y_botao = self.y + (self.ALTURA - self.ALTURA_BOTAO_FILTRO) // 2
        return Botao("EDITAR", x_editar, y_botao, self.LARGURA_BOTAO_EDITAR, self.ALTURA_BOTAO_FILTRO, Cores.BOTAO_EDITAR, Cores.TEXTO_BOTOES, "editar")

    def desenhar(self, tela):
        pygame.draw.rect(tela, Cores.LISTA_ITEM, self.rect, border_radius=5)
        tela.blit(self.texto_renderizado, self.texto_rect)
        for botao in self.botoes_filtro:
            botao.desenhar(tela)
        self.botao_editar.desenhar(tela)

    def verificar_clique_botoes(self, pos_mouse):
        for botao in self.botoes_filtro:
            if botao.verificar_clique(pos_mouse):
                print(f"Botão '{botao.texto}' da lista clicado. Função: {botao.funcao}")
                return True
        if self.botao_editar.verificar_clique(pos_mouse):
            print(f"Botão '{self.botao_editar.texto}' da lista clicado. Função: {self.botao_editar.funcao}")
            return True
        return False