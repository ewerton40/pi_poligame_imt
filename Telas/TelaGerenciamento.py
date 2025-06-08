import pygame
import os 
from UI.Botao import Botao
from Classes.item_lista import ItemLista
from Telas.TelaAddAluno import TelaAddAluno
from Telas.TelaAddPergunta import AddPerguntaTela
from Telas.TelaAddProfessor import TelaAddProfessor
from Telas.TelaRanking import RankingTela 
from interfaces.database import Database

class TelaGerenciamento:
    def __init__(self, screen, transition_call):
        pygame.init()
        self.largura = 1280
        self.altura = 720
        self.screen = screen
        self.transition_call = transition_call
        self.is_loaded = False
        self.db_manager = Database()
        self.db_manager.connect()
        texto_mostrar = "Perguntas"
        self.fonte = pygame.font.Font(None, 30)
        self.texto_mostrar = self.fonte.render(texto_mostrar, True, pygame.Color("black"))
        self.rect_mostrar = self.texto_mostrar.get_rect(
            topleft=(10, 20 + 60 + 20)
        )

    
        self.botoes_menu = self._criar_botoes_menu()
        self.espacamento_lista = 10
        self.y_inicial_lista = self.rect_mostrar.bottom + 20
         
        self.scroll_area_rect = pygame.Rect(
            10, self.y_inicial_lista, self.largura - 20, self.altura - self.y_inicial_lista - 20
        )
        self.scroll_offset = 0
        self.scroll_speed = 20

        self._atualizar_lista_itens()
        self.rodando = True


    def load(self):
        self._atualizar_lista_itens()
        self.is_loaded = True

    def run(self, events):
        self._atualizar_lista_itens()
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        self.executar()


    def _criar_botoes_menu(self):
        labels = ["Criar", "Filtrar", "Add Aluno", "Add Professor", "Ranking"]
        num = len(labels)

        largura_botao = 140
        altura_menu = 60
        espaco_lateral = self.largura - (num * largura_botao)
        espacamento = espaco_lateral // (num + 1)

        botoes = []
        x = espacamento
        for texto in labels:
            func = texto.lower().replace(" ", "_")
            cor_botao = pygame.Color("skyblue")
            botao = Botao(
                pos=(x, 20),
                size=(largura_botao, altura_menu),
                color=cor_botao,
                text=texto,
                font=self.fonte
            )
            botao.funcao = func
            botoes.append(botao)
            x += largura_botao + espacamento
        return botoes
    

    def _listar_perguntas_db(self):
        return self.db_manager.get_all_questions_details()
        
    def _excluir_pergunta_db(self, pergunta_id: int):
        self.db_manager.delete_questao(pergunta_id)
        
    def _close_db_connection(self):
        self.db_manager.close()

    def _atualizar_lista_itens(self, filtrar_por_materia_id=None):    
        if filtrar_por_materia_id:
            perguntas = self.db_manager.get_questions_by_materia(filtrar_por_materia_id)
        else:
            perguntas = self._listar_perguntas_db()
        self.itens_lista = []
        for i, pergunta_data in enumerate(perguntas):
            item_y = self.content_height = len(self.itens_lista) * (70 + self.espacamento_lista) 
            item = ItemLista(
                pergunta_data,
                item_y,
                self.largura,
                on_excluir=self._acao_excluir_pergunta
            )
            self.itens_lista.append(item)

        self.content_height = len(self.itens_lista) * (70 + self.espacamento_lista)
        self._ajustar_scroll_offset()
        


    def _ajustar_scroll_offset(self):
        if self.content_height < self.scroll_area_rect.height:
            self.scroll_offset = 0
        else:
            self.scroll_offset = max(self.scroll_area_rect.height - self.content_height, self.scroll_offset)
            self.scroll_offset = min(0, self.scroll_offset)

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                self._close_db_connection()
            
            self._processar_eventos_mouse(evento)

    def _processar_eventos_mouse(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            self._processar_clique_botao(evento)
            self._processar_scroll(evento)
            self._processar_clique_lista(evento)

    def _processar_clique_botao(self, evento):
        for botao in self.botoes_menu:
            if botao.rect.collidepoint(evento.pos):
                if botao.funcao == "criar":
                    self._acao_criar()
                elif botao.funcao == "ranking":
                    self._acao_ranking()
                elif botao.funcao == "add_aluno":
                    self._acao_adicionar_aluno()
                elif botao.funcao == "add_professor":
                    self._acao_adicionar_professor()
                elif botao.funcao == "filtrar":
                    self._acao_filtrar()

    def _processar_scroll(self, evento):
        if evento.button == 4:  # Scroll up
            self.scroll_offset = min(self.scroll_offset + self.scroll_speed, 0)
        elif evento.button == 5:  # Scroll down
            max_offset = self.scroll_area_rect.height - self.content_height
            self.scroll_offset = max(self.scroll_offset - self.scroll_speed, max_offset)

    def _processar_clique_lista(self, evento):
        if self.scroll_area_rect.collidepoint(evento.pos):
            relative_mouse_pos = (
                evento.pos[0] - self.scroll_area_rect.x,
                evento.pos[1] - self.scroll_area_rect.y - self.scroll_offset
            )
            for item in self.itens_lista:
                if item.verificar_clique_botoes(relative_mouse_pos):
                    break

    def _renderizar_tela(self):
        self.tela.fill(pygame.Color("lightgray"))

        # Desenhar botões do menu
        for botao in self.botoes_menu:
            botao.draw(self.tela)

        # Desenhar título
        self.tela.blit(self.texto_mostrar, self.rect_mostrar)

        # Desenhar lista com scroll
        self._renderizar_lista()

        pygame.display.flip()

    def _renderizar_lista(self):
        list_surface = pygame.Surface((self.scroll_area_rect.width, max(self.scroll_area_rect.height, self.content_height)))
        list_surface.fill(pygame.Color("lightgray")) 

        # Desenhar itens na superfície da lista
        for item in self.itens_lista:
            item.desenhar(list_surface, self.scroll_offset) 

        # Desenhar a área visível da lista na tela principal
        self.tela.blit(
            list_surface, 
            self.scroll_area_rect, 
            (0, -self.scroll_offset, self.scroll_area_rect.width, self.scroll_area_rect.height)
        )
        pygame.display.flip()

    def executar(self):
        while self.rodando:
            self._processar_eventos()
            self._renderizar_tela()

        pygame.quit()
        self._close_db_connection()

    def _acao_filtrar(self):
        import tkinter as tk

        materias = self.db_manager.get_materias()
        if not materias:
            print("Nenhuma matéria encontrada no banco.")
            return

        # Criar uma janela tkinter para exibir os botões
        root = tk.Tk()
        root.title("Filtrar por Matéria")
        root.geometry("300x400")
        root.configure(bg="white")

        label = tk.Label(root, text="Selecione uma matéria:", bg="white", font=("Arial", 14))
        label.pack(pady=10)

        def selecionar_materia(materia_id):
            root.destroy()  # Fecha a janela
            self._atualizar_lista_itens(filtrar_por_materia_id=materia_id)

        for materia in materias:
            nome = materia["nome"].capitalize()
            materia_id = materia["id"]
            botao = tk.Button(root, text=nome, width=25, height=2, bg="#ADD8E6", command=lambda m=materia_id: selecionar_materia(m))
            botao.pack(pady=5)

        root.mainloop()



    def _acao_criar(self):
        perguntas_antes = len(self.db_manager.get_all_questions_details())
        tela_add = AddPerguntaTela()
        tela_add.executar()
        perguntas_depois = len(self.db_manager.get_all_questions_details())
        self._atualizar_lista_itens()

    def _acao_ranking(self):
        """Abre a tela de ranking"""
        try:
            janela_ranking = RankingTela(tela_principal=self.tela)
            janela_ranking.executar()  # Remova o argumento tela_principal aqui também
        except Exception as e:
            print(f"Erro ao abrir tela de ranking: {e}")

    def _acao_adicionar_aluno(self):
        """Abre a tela para adicionar novo professor"""
        try:
            tela_adicionar = TelaAddAluno(
                screen=self.tela,
                transition_call=lambda: print("Transição chamada")
            )
            tela_adicionar.executar(tela_principal=self.tela)
        except Exception as e:
            print(f"Erro ao abrir tela de adicionar professor: {e}")

    def _acao_adicionar_professor(self):
        """Abre a tela para adicionar novo professor"""
        try:
            tela_adicionar = TelaAddProfessor(
                screen=self.tela,
                transition_call=lambda: print("Transição chamada")
            )
            tela_adicionar.executar(tela_principal=self.tela)
        except Exception as e:
            print(f"Erro ao abrir tela de adicionar professor: {e}")

    def _acao_excluir_pergunta(self, pergunta_id):
        self._excluir_pergunta_db(pergunta_id)
        self._atualizar_lista_itens()