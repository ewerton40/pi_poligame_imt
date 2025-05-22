
import pygame
from .botao import Botao
from .item_lista import ItemLista
from .gerenciador_perguntas import GerenciadorPerguntas
from rankingAlunos import abrir_janela2
from adicionarAluno import abrir_tela_adicionar_aluno
from addPerguntaTela import abrir_nova_janela

# Fontes locais
FONTE_PADRAO = pygame.font.Font(None, 30)
FONTE_PEQUENA = pygame.font.Font(None, 24)

class TelaGerenciamento:
    MARGEM_SUPERIOR = 20
    ALTURA_MENU = 60
    LARGURA_BOTAO_MENU = 140
    ESPACAMENTO_MENU = 10

    def __init__(self):
        pygame.init()
        # Dimensões da tela
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Tela de Gerenciamento")

        # Botões do menu superior
        self.botoes_menu = self._criar_botoes_menu()

        # Texto informativo
        self.texto_mostrar = FONTE_PADRAO.render("Perguntas", True, pygame.Color("black"))
        self.rect_mostrar = self.texto_mostrar.get_rect(
            topleft=(self.ESPACAMENTO_MENU, self.MARGEM_SUPERIOR + self.ALTURA_MENU + 20)
        )

        # Gerenciador de perguntas e lista
        self.gerenciador_perguntas = GerenciadorPerguntas()
        self.espacamento_lista = 10
        self.y_inicial_lista = self.rect_mostrar.bottom + 20
        self._atualizar_lista_itens()

        self.rodando = True

    def _criar_botoes_menu(self):
        num = 5
        largura_total = num * self.LARGURA_BOTAO_MENU
        espaco = self.largura - largura_total
        esp_uniforme = espaco // (num + 1)

        labels = ["Criar", "Procurar", "Filtrar", "Add Aluno", "Ranking"]
        botoes = []
        x = self.largura - esp_uniforme - self.LARGURA_BOTAO_MENU
        for texto in reversed(labels):
            func = texto.lower().replace(" ", "_")
            # cores inline
            cor_botao = pygame.Color("dimgray")
            cor_texto = pygame.Color("white")
            botao = Botao(texto, x, self.MARGEM_SUPERIOR, self.LARGURA_BOTAO_MENU, self.ALTURA_MENU,
                          cor_botao, cor_texto, func)
            botoes.append(botao)
            x -= self.LARGURA_BOTAO_MENU + esp_uniforme
        return list(reversed(botoes))

    def _atualizar_lista_itens(self):
        perguntas = self.gerenciador_perguntas.listar_perguntas()
        self.itens_lista = [
            ItemLista(pergunta, self.y_inicial_lista + i * (ItemLista.ALTURA + self.espacamento_lista), self.largura)
            for i, pergunta in enumerate(perguntas)
        ]

    def executar(self):
        while self.rodando:
            self.tela.fill(pygame.Color("lightgray"))
            # Desenha menu e texto
            for botao in self.botoes_menu:
                botao.desenhar(self.tela)
            self.tela.blit(self.texto_mostrar, self.rect_mostrar)
            # Desenha lista
            for item in self.itens_lista:
                item.desenhar(self.tela)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Menu
                    for botao in self.botoes_menu:
                        if botao.verificar_clique(pos):
                            if botao.funcao == "criar":
                                self._acao_criar()
                            elif botao.funcao == "ranking":
                                self._acao_ranking()
                            elif botao.funcao == "add_aluno":
                                self._acao_adicionar_aluno()
                    # Itens da lista
                    for item in self.itens_lista:
                        item.verificar_clique_botoes(pos)
        pygame.quit()

    def _acao_criar(self):
        retorno = abrir_nova_janela(self.tela)
        if retorno == "adicionar":
            self.gerenciador_perguntas.adicionar_pergunta("Nova Pergunta")
            self._atualizar_lista_itens()

    def _acao_ranking(self):
        if not abrir_janela2(self.tela):
            self.rodando = False

    def _acao_adicionar_aluno(self):
        abrir_tela_adicionar_aluno(self.tela)

if __name__ == '__main__':
    tela = TelaGerenciamento()
    tela.executar()
