import pygame
from .elementos_visuais import Cores, DimensaoTela, Fonte
from .botao import Botao
from .item_lista import ItemLista
from .gerenciador_perguntas import GerenciadorPerguntas
from rankingAlunos import abrir_janela2  # Importe da raiz!
from adicionarAluno import abrir_tela_adicionar_aluno
from addPerguntaTela import abrir_nova_janela

class TelaGerenciamento:
    MARGEM_SUPERIOR = 20
    ALTURA_MENU = 60
    LARGURA_BOTAO_MENU = 140
    ESPACAMENTO_MENU = 10

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((DimensaoTela.LARGURA, DimensaoTela.ALTURA))
        pygame.display.set_caption("Tela de Gerenciamento")
        self.botoes_menu = self._criar_botoes_menu()
        self.texto_mostrar = Fonte.PADRAO.render("Perguntas", True, (0, 0, 0))
        self.rect_mostrar = self.texto_mostrar.get_rect(topleft=(self.ESPACAMENTO_MENU, self.MARGEM_SUPERIOR + self.ALTURA_MENU + 20))
        self.gerenciador_perguntas = GerenciadorPerguntas() # Inicializa o gerenciador de perguntas
        self.espacamento_lista = 10
        self.y_inicial_lista = self.rect_mostrar.bottom + 20
        self._atualizar_lista_itens() # Atualiza a lista de itens com as perguntas do gerenciador
        self.rodando = True

class TelaGerenciamento:
    MARGEM_SUPERIOR = 20
    ALTURA_MENU = 60
    LARGURA_BOTAO_MENU = 140
    ESPACAMENTO_MENU = 10

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((DimensaoTela.LARGURA, DimensaoTela.ALTURA))
        pygame.display.set_caption("Tela de Gerenciamento")
        self.botoes_menu = self._criar_botoes_menu()
        self.texto_mostrar = Fonte.PADRAO.render("Perguntas", True, (0, 0, 0))
        self.rect_mostrar = self.texto_mostrar.get_rect(topleft=(self.ESPACAMENTO_MENU, self.MARGEM_SUPERIOR + self.ALTURA_MENU + 20))
        self.gerenciador_perguntas = GerenciadorPerguntas() # Inicializa o gerenciador de perguntas
        self.espacamento_lista = 10
        self.y_inicial_lista = self.rect_mostrar.bottom + 20
        self._atualizar_lista_itens() # Atualiza a lista de itens com as perguntas do gerenciador
        self.rodando = True

    def _criar_botoes_menu(self):
        num_botoes_menu = 5
        largura_total_botoes = num_botoes_menu * self.LARGURA_BOTAO_MENU
        espaco_disponivel = DimensaoTela.LARGURA - largura_total_botoes
        num_espacos = num_botoes_menu + 1
        espacamento_uniforme = espaco_disponivel // num_espacos

        botoes_data = []
        x_atual = DimensaoTela.LARGURA - espacamento_uniforme - self.LARGURA_BOTAO_MENU
        for texto_botao in reversed(["Criar", "Procurar", "Filtrar", "Add Aluno", "Ranking"]):
            funcao = texto_botao.lower().replace(" ", "_")
            botao = Botao(texto_botao, x_atual, self.MARGEM_SUPERIOR, self.LARGURA_BOTAO_MENU, self.ALTURA_MENU, Cores.BOTOES_MENU, Cores.TEXTO_BOTOES, funcao)
            botoes_data.append(botao)
            x_atual -= self.LARGURA_BOTAO_MENU + espacamento_uniforme
        return list(reversed(botoes_data)) # Retorna na ordem original

    def _atualizar_lista_itens(self):
        self.itens_lista = [ItemLista(pergunta, self.y_inicial_lista + i * (ItemLista.ALTURA + self.espacamento_lista), DimensaoTela.LARGURA) for i, pergunta in enumerate(self.gerenciador_perguntas.listar_perguntas())]

    def criar_novo_elemento(self):
        """Esta função será executada quando o botão 'Criar' for clicado e abrirá a nova janela."""
        print("Botão 'Criar' foi clicado! Abrindo nova janela.")
        retorno_janela_criar = abrir_nova_janela(self.tela)
        if retorno_janela_criar == "cancelar":
            print("Criação de pergunta cancelada.")
        elif retorno_janela_criar == "adicionar":
            texto_nova_pergunta = "Nova Pergunta da Tela de Criação" # Substitua pela lógica real de obter a pergunta
            self.gerenciador_perguntas.adicionar_pergunta(texto_nova_pergunta)
            self._atualizar_lista_itens()
        elif retorno_janela_criar == "fechar_janela":
            print("Janela de adicionar pergunta fechada.")

    def adicionar_pergunta_chamado(self):
        print("Botão 'Add Pergunta' clicado! Abrindo tela de adicionar pergunta.")
        retorno_adicionar_pergunta = abrir_nova_janela(self.tela)
        print(f"Retorno da tela de adicionar pergunta: {retorno_adicionar_pergunta}")

    def ranking_alunos_chamado(self):
        print("Botão 'Ranking' clicado! Abrindo tela de ranking.")
        voltar_para_principal = abrir_janela2(self.tela)
        if voltar_para_principal:
            print("Voltou para a tela principal.")


    def ranking_alunos_chamado(self):
        """Esta função será executada quando o botão 'ranking' for clicado e abrirá a tela de ranking."""
        print("Botão 'ranking' foi clicado! Abrindo tela de ranking.")
        retorno_ranking = abrir_janela2(self.tela)
        if not retorno_ranking:
            self.rodando = False

    def adicionar_aluno_chamado(self):
        """Função para abrir a tela de adicionar aluno."""
        print("Botão 'Add Aluno' clicado! Abrindo tela de adicionar aluno.")
        retorno_adicionar_aluno = abrir_tela_adicionar_aluno(self.tela)
        if retorno_adicionar_aluno == "cancelar":
            print("Adição de aluno cancelada.")
        elif retorno_adicionar_aluno == "adicionar_aluno":
            print("Dados do aluno a serem processados.")
            pass
        elif retorno_adicionar_aluno == "fechar_janela":
            print("Janela de adicionar aluno fechada.")

    def ranking_alunos_chamado(self):
        print("Botão 'Ranking' clicado! Abrindo tela de ranking.")
        voltar_para_principal = abrir_janela2(self.tela)
        if voltar_para_principal:
            print("Voltou para a tela principal.")


    def executar(self):
        while self.rodando:
            self.tela.fill(Cores.FUNDO)

            # Desenha os botões do menu superior
            for botao in self.botoes_menu:
                botao.desenhar(self.tela)

            # Desenha o label "Mostrar"
            self.tela.blit(self.texto_mostrar, self.rect_mostrar)

            # Desenha a lista de perguntas
            for item in self.itens_lista:
                item.desenhar(self.tela)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    for botao in self.botoes_menu:
                        if botao.verificar_clique(pos_mouse):
                            print(f"Botão '{botao.texto}' clicado. Função: {botao.funcao}")
                            if botao.funcao == "criar":
                                self.criar_novo_elemento()
                            elif botao.funcao == "ranking":
                                self.ranking_alunos_chamado()
                            elif botao.funcao == "add_aluno":
                                self.adicionar_aluno_chamado()

                    for item in self.itens_lista:
                        item.verificar_clique_botoes(pos_mouse)

        pygame.quit()