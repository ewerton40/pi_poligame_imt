import pygame
from UI.Botao import Botao
from ..Classes.item_lista import ItemLista
from ..Classes.gerenciador_perguntas import GerenciadorPerguntas
from Telas.TelaRanking import TelaRanking
from TelaAddAluno import TelaAddAluno
from TelaAddPergunta import AddPerguntaTela 

class TelaGerenciamento:
    def __init__(self):
        pygame.init()
        self.largura = 800
        self.altura = 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Tela de Gerenciamento")

        self.botoes_menu = self._criar_botoes_menu()

        fonte_padrao = pygame.font.Font(None, 30)
        self.texto_mostrar = fonte_padrao.render("Perguntas", True, pygame.Color("black"))
        self.rect_mostrar = self.texto_mostrar.get_rect(
            topleft=(10, 20 + 60 + 20)  # ESPACAMENTO_MENU=10, MARGEM_SUPERIOR=20, ALTURA_MENU=60
        )

        self.gerenciador_perguntas = GerenciadorPerguntas()
        self.espacamento_lista = 10
        self.y_inicial_lista = self.rect_mostrar.bottom + 20
        self._atualizar_lista_itens()

        self.rodando = True

    def _criar_botoes_menu(self):
        num = 5
        largura_total = num * 140  # LARGURA_BOTAO_MENU
        espaco = self.largura - largura_total
        esp_uniforme = espaco // (num + 1)

        labels = ["Criar", "Procurar", "Filtrar", "Add Aluno", "Ranking"]
        botoes = []
        x = self.largura - esp_uniforme - 140  # LARGURA_BOTAO_MENU
        for texto in reversed(labels):
            func = texto.lower().replace(" ", "_")
            cor_botao = pygame.Color("dimgray")
            cor_texto = pygame.Color("white")
            botao = Botao(texto, x, 20, 140, 60, cor_botao, cor_texto, func)  # MARGEM_SUPERIOR=20, LARGURA/ALTURA_BOTAO_MENU
            botoes.append(botao)
            x -= 140 + esp_uniforme
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
            for botao in self.botoes_menu:
                botao.desenhar(self.tela)
            self.tela.blit(self.texto_mostrar, self.rect_mostrar)

            for item in self.itens_lista:
                item.desenhar(self.tela)
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for botao in self.botoes_menu:
                        if botao.verificar_clique(pos):
                            if botao.funcao == "criar":
                                self._acao_criar()
                            elif botao.funcao == "ranking":
                                self._acao_ranking()
                            elif botao.funcao == "add_aluno":
                                self._acao_adicionar_aluno()
                    for item in self.itens_lista:
                        item.verificar_clique_botoes(pos)
        pygame.quit()

    def _acao_criar(self):
        tela_add = AddPerguntaTela()
        retorno = tela_add.executar()
        if retorno == "adicionar":
            self.gerenciador_perguntas.adicionar_pergunta("Nova Pergunta")
            self._atualizar_lista_itens()

    def _acao_ranking(self):
        janela_ranking = TelaRanking(self.tela)
        if not janela_ranking.executar():
            self.rodando = False

    def _acao_adicionar_aluno(self):
        tela_adicionar = TelaAddAluno()
        retorno = tela_adicionar.executar(self.tela)
        print(f"Retorno da tela adicionar aluno: {retorno}")

if __name__ == '__main__':
    tela = TelaGerenciamento()
    tela.executar()
