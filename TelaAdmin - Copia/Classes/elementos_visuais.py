import pygame

# Arquivo: elementos_visuais.py
import pygame

class Cores:
    FUNDO = (220, 220, 220)
    BOTOES_MENU = (80, 80, 80)
    TEXTO_BOTOES = (255, 255, 255)
    TEXTO = (255, 255, 255)  # Branco
    TEXTO_BOTAO = (255, 255, 255)
    LISTA_ITEM = (50, 50, 50)
    TEXTO_LISTA = (255, 255, 255)
    BOTAO_FILTRO = (128, 128, 128)
    BOTAO_EDITAR = (160, 82, 45)
    BOTAO_FECHAR = (160, 82, 45)
    BORDA_CAIXA_TEXTO_ATIVO = (0, 128, 255)  # Azul claro (borda da caixa de texto ativa)
    BORDA_CAIXA_TEXTO_INATIVO = (100, 100, 100)  # Cinza médio (borda da caixa de texto inativa)
    CAIXA_TEXTO_FUNDO = (50, 50, 50) # Adicionado COR_CAIXA_TEXTO_FUNDO
    BORDA_CAIXA_TEXTO_ATIVO = (0, 128, 255)
    BORDA_CAIXA_TEXTO_INATIVO = (100, 100, 100)
    COR_FILTRO_SELECIONADO = (100, 200, 100)
    COR_FILTRO_NAO_SELECIONADO = (200, 100, 100)
    TEXTO_CABECALHO = (255, 255, 255)
    CABECALHO = (80, 80, 80)
    TEXTO_FECHAR = (255, 255, 255)
    LINHA = (100,100,100)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    BUTTON_COLOR = (50, 50, 50)
    BUTTON_HOVER = (80, 80, 80)
    SELECTED_COLOR = (100, 150, 200)

class DimensaoTela:
    LARGURA = 800
    ALTURA = 600

class Fonte:
    PADRAO = pygame.font.Font(None, 30)
    PEQUENA = pygame.font.Font(None, 24)
    CABECALHO = pygame.font.Font(None, 22)  # Diminuindo a fonte do cabeçalho
    FECHAR = pygame.font.Font(None, 20)  # Diminuindo a fonte do botão fechar

    TITULO = None
    TEXTO = None

    _inicializado = False

    @staticmethod
    def inicializar():
        if not Fonte._inicializado:
            pygame.font.init()
            Fonte.PADRAO = pygame.font.Font(None, 30)
            Fonte.PEQUENA = pygame.font.Font(None, 24)
            Fonte.CABECALHO = pygame.font.Font(None, 22)
            Fonte.FECHAR = pygame.font.Font(None, 20)
            Fonte.TITULO = pygame.font.Font(None, 60)
            Fonte.TEXTO = pygame.font.Font(None, 24)
            Fonte._inicializado = True

    @staticmethod
    def get_PADRAO():
        Fonte.inicializar()
        return Fonte.PADRAO

    @staticmethod
    def get_PEQUENA():
        Fonte.inicializar()
        return Fonte.PEQUENA

    @staticmethod
    def get_CABECALHO():
        Fonte.inicializar()
        return Fonte.CABECALHO

    @staticmethod
    def get_FECHAR():
        Fonte.inicializar()
        return Fonte.FECHAR

    @staticmethod
    def get_TITULO():
        Fonte.inicializar()
        return Fonte.TITULO

    @staticmethod
    def get_TEXTO():
        Fonte.inicializar()
        return Fonte.TEXTO

class Botao:
    def __init__(self, texto, x, y, largura, altura, cor, cor_texto, funcao=None):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_texto = cor_texto
        self.funcao = funcao
        self.texto_renderizado = Fonte.PADRAO.render(texto, True, cor_texto)
        self.texto_rect = self.texto_renderizado.get_rect(center=self.rect.center)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect, border_radius=5)
        tela.blit(self.texto_renderizado, self.texto_rect)

    def verificar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

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
        botao1 = Botao("Filtro()", ...) # Na criação, já usará o getter
        botao2 = Botao("Filtro()", ...)
        botao3 = Botao("Filtro()", ...)
        self.botao_editar = self._criar_botao_editar()

        self.texto_rect = self.texto_renderizado.get_rect(midleft=(self.x_item + self.MARGEM, y + self.ALTURA // 2))
        self.botoes_filtro = self._criar_botoes_filtro()
        self.botao_editar = self._criar_botao_editar()
        self.botoes_rects = [botao.rect for botao in self.botoes_filtro] + [self.botao_editar.rect]


    def _criar_botao_editar(self):
        return Botao("EDITAR", ...) # Na criação, já usará o getter


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
    
def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    tela.blit(texto_renderizado, texto_rect)

def escalar(valor, resolucao_original_x, resolucao_desejada_x):
    return int(valor * (resolucao_desejada_x / resolucao_original_x))

def escalar_y(valor, resolucao_original_y, resolucao_desejada_y):
    return int(valor * (resolucao_desejada_y / resolucao_original_y))