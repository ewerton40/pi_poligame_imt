import pygame
from UI.Botao import Botao

class ItemLista:
    ALTURA = 50
    MARGEM = 10
    ALTURA_BOTAO = 30
    LARGURA_BOTAO_EDITAR = 80

    def __init__(self, texto_pergunta, y, largura_total):
        self.largura_total = largura_total
        self.y = y
        self.x_item = self.MARGEM
        self.largura_item = largura_total - 2 * self.MARGEM
        self.rect = pygame.Rect(self.x_item, y, self.largura_item, self.ALTURA)

        # Fonte padrão
        self.fonte = pygame.font.Font(None, 30)

        # Texto da pergunta
        cor_texto = pygame.Color("white")
        self.texto_renderizado = self.fonte.render(texto_pergunta, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(
            midleft=(self.x_item + self.MARGEM, y + self.ALTURA // 2)
        )

        # Botão de editar
        self.botao_editar = self._criar_botao_editar()

    def _criar_botao_editar(self):
        cor_editar = pygame.Color("saddlebrown")
        x_editar = self.x_item + self.largura_item - self.LARGURA_BOTAO_EDITAR - self.MARGEM
        y_botao = self.y + (self.ALTURA - self.ALTURA_BOTAO) // 2
        botao = Botao((x_editar, y_botao), (self.LARGURA_BOTAO_EDITAR, self.ALTURA_BOTAO), cor_editar, "EDITAR", self.fonte)
        botao.funcao = "editar"
        return botao

    def desenhar(self, tela):
        cor_fundo = pygame.Color("darkgray")
        pygame.draw.rect(tela, cor_fundo, self.rect, border_radius=5)

        tela.blit(self.texto_renderizado, self.texto_rect)
        self.botao_editar.draw(tela)

    def verificar_clique_botoes(self, pos_mouse):
        if self.botao_editar.check_button():
            print(f"Botão '{self.botao_editar.text}' da lista clicado. Função: {self.botao_editar.funcao}")
            return True
        return False