import pygame
from Botao import Botao

# Fonte padrão

class ItemLista:
    def __init__(self, texto_pergunta, y, largura_total):
        self.largura_total = largura_total
        self.y = y
        self.x_item = 10  # MARGEM
        self.largura_item = largura_total - 2 * 10
        self.rect = pygame.Rect(self.x_item, y, self.largura_item, 50)  # ALTURA = 50

        # Fonte usada nos botões
        self.fonte = pygame.font.Font(None, 24)

        # Renderiza texto da pergunta
        cor_texto = pygame.Color("white")
        self.texto_renderizado = pygame.font.Font(None, 30).render(texto_pergunta, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(
            midleft=(self.x_item + 10, y + 50 // 2)  # MARGEM + ALTURA//2
        )

        # Botões de filtro e editar
        self.botoes_filtro = self._criar_botoes_filtro()
        self.botoes_filtro_funcoes = ["filtrar", "filtrar", "filtrar"]
        self.botao_editar = self._criar_botao_editar()
        self.funcao_editar = "editar"
        self.botoes_rects = [botao.rect for botao in self.botoes_filtro] + [self.botao_editar.rect]

    def _criar_botoes_filtro(self):
        cor_filtro = pygame.Color("gray")

        largura_botao = 80
        altura_botao = 30
        espacamento = 30
        margem = 10

        x_base = self.x_item + self.largura_item - margem - largura_botao
        positions = [
            x_base - 2 * (largura_botao + espacamento),
            x_base - (largura_botao + espacamento),
            x_base,
        ]
        y_botao = self.y + (50 - altura_botao) // 2  # ALTURA - altura_botao

        botoes = []
        for x in positions:
            botoes.append(
                Botao(
                    (x, y_botao),
                    (largura_botao, altura_botao),
                    cor_filtro,
                    "Filtro()",
                    self.fonte
                )
            )
        return botoes

    def _criar_botao_editar(self):
        cor_editar = pygame.Color("saddlebrown")

        largura_botao = 80
        altura_botao = 30
        margem = 10

        x_editar = (
            self.x_item + self.largura_item - largura_botao - margem
        )
        y_botao = self.y + (50 - altura_botao) // 2  # ALTURA - altura_botao
        return Botao(
            (x_editar, y_botao),
            (largura_botao, altura_botao),
            cor_editar,
            "EDITAR",
            self.fonte
        )

    def desenhar(self, tela):
        cor_fundo = pygame.Color("darkgray")
        pygame.draw.rect(tela, cor_fundo, self.rect, border_radius=5)

        tela.blit(self.texto_renderizado, self.texto_rect)
        for botao in self.botoes_filtro:
            botao.draw(tela)
        self.botao_editar.draw(tela)

    def verificar_clique_botoes(self):
        for i, botao in enumerate(self.botoes_filtro):
            if botao.check_button():
                print(f"Botão '{botao.text}' da lista clicado. Função: {self.botoes_filtro_funcoes[i]}")
                return True
        if self.botao_editar.check_button():
            print(f"Botão '{self.botao_editar.text}' da lista clicado. Função: {self.funcao_editar}")
            return True
        return False
    
    def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
        texto_renderizado = pygame.font.Font(None, 30).render(texto, True, cor)
        texto_rect = texto_renderizado.get_rect(center=rect.center)
        tela.blit(texto_renderizado, texto_rect)
