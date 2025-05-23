import pygame
from ..Classes.botao import Botao
from ..Classes.item_lista import ItemLista
from ..Classes.gerenciador_perguntas import GerenciadorPerguntas
from Telas.TelaRanking import TelaRanking
from TelaAddAluno import TelaAddAluno
from TelaAddPergunta import AddPerguntaTela 

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
        fonte_padrao = pygame.font.Font(None, 30)
        self.texto_mostrar = fonte_padrao.render("Perguntas", True, pygame.Color("black"))
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
        # Cria uma instância da classe AddPerguntaTela
        tela_add = AddPerguntaTela()
        # Executa a interface e espera o resultado
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
        # Opcional: faça algo com o retorno, ex:
        print(f"Retorno da tela adicionar aluno: {retorno}")

if __name__ == '__main__':
    tela = TelaGerenciamento()
    tela.executar()
