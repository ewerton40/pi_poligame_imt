import pygame
from .botao import Botao

# Fonte padrão

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

        # Renderiza texto da pergunta
        cor_texto = pygame.Color("white")
        self.texto_renderizado = pygame.font.Font(None, 30).render(texto_pergunta, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(
            midleft=(self.x_item + self.MARGEM, y + self.ALTURA // 2)
        )

        # Botões de filtro e editar
        self.botoes_filtro = self._criar_botoes_filtro()
        self.botao_editar = self._criar_botao_editar()
        self.botoes_rects = [botao.rect for botao in self.botoes_filtro] + [self.botao_editar.rect]

    def _criar_botoes_filtro(self):
        # Cores inline para botões de filtro
        cor_filtro = pygame.Color("gray")
        cor_texto = pygame.Color("white")

        x_base = self.x_item + self.largura_item - self.MARGEM - self.LARGURA_BOTAO_FILTRO
        positions = [
            x_base - 2 * (self.LARGURA_BOTAO_FILTRO + self.ESPACAMENTO_FILTRO),
            x_base - (self.LARGURA_BOTAO_FILTRO + self.ESPACAMENTO_FILTRO),
            x_base,
        ]
        y_botao = self.y + (self.ALTURA - self.ALTURA_BOTAO_FILTRO) // 2

        botoes = []
        for x in positions:
            botoes.append(
                Botao(
                    "Filtro()", x, y_botao,
                    self.LARGURA_BOTAO_FILTRO, self.ALTURA_BOTAO_FILTRO,
                    pygame.Color("gray"), pygame.Color("white"),
                    "filtrar"
                )
            )
        return botoes

    def _criar_botao_editar(self):
        # Cores inline para botão editar
        cor_editar = pygame.Color("saddlebrown")
        cor_texto = pygame.Color("white")

        x_editar = (
            self.x_item + self.largura_item - self.LARGURA_BOTAO_EDITAR - self.MARGEM
        )
        y_botao = self.y + (self.ALTURA - self.ALTURA_BOTAO_FILTRO) // 2
        return Botao(
            "EDITAR", x_editar, y_botao,
            self.LARGURA_BOTAO_EDITAR, self.ALTURA_BOTAO_FILTRO,
            cor_editar, cor_texto, "editar"
        )

    def desenhar(self, tela):
        # Cor inline para fundo do item da lista
        cor_fundo = pygame.Color("darkgray")
        pygame.draw.rect(tela, cor_fundo, self.rect, border_radius=5)

        # Desenha texto e botões
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
