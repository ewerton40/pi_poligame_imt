import pygame
import json
import random
from UI.Botao import Botao
from UI.DicaBotao import DicaBotao
from UI.Pontuacao import Pontuacao
from Telas.Tela import Tela
from Telas.TelaAcerto import TelaAcerto
from Classes.Pergunta import Pergunta# Classe que gerencia perguntas
from util import WINDOW_SIZE, break_line, DATABASE, USER

class TelaPergunta(Tela):
    def __init__(self, screen, transition_call, id_materia, quit_game, id_partida ):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.ended = False
        self.acertos = 0
        self.images = {}
        self.texts = []
        self.answer_btn = []
        self.id_materia = id_materia
        self.id_partida = id_partida
        self.quit_game = quit_game
        self.checkpoint = 0  # valor salvo ao atingir o checkpoint
        self.pergunta_atual = 1
        self.fonte = pygame.font.SysFont("Arial", 25)

        # Verifica se já existe entrada na tabela Dica para essa partida
        dica_existente = DATABASE.get_dica_por_partida(self.id_partida)
        if not dica_existente:
            DATABASE.criar_dica_para_partida(self.id_partida)

        # Flags locais de uso (evita múltiplos cliques)
        self.usou_meio = dica_existente["MeioaMeio"] if dica_existente else False
        self.usou_pular = dica_existente["PularDica"] if dica_existente else False

    def load(self):
        questions = DATABASE.get_questoes_por_materia_json(self.id_materia)
        perguntas = json.loads(questions)
        random.shuffle(perguntas)
        selected_questions = perguntas[:10]
        #Cria um pool de perguntas
        self.pool = Pergunta(selected_questions)
        self.text = self.pool.get_question() #Pega a primeira pergunta
        self.answers:list[dict] = self.pool.get_answers() #Pega as respostas para compará-las com a pergunta
        self.score = Pontuacao((1035, 10), (150, 50), pygame.Color("red"))
        self.len_questions = len(self.pool.questions) 

        self.images = {
            "background": pygame.image.load("imagens/pergunta.jpg").convert_alpha(),
        }

        self.pular_btn = DicaBotao((900, 640),pygame.image.load("imagens/pular.png").convert_alpha(), 
                                  pygame.image.load("imagens/pular_usado.png").convert_alpha())


        self.meio_a_meio_btn = DicaBotao((820, 640), pygame.image.load("imagens/meio.png").convert_alpha(),
                                         pygame.image.load("imagens/meio_usado.png").convert_alpha())
        
        self.parar_btn = Botao((1035, 600), (100, 45), pygame.Color("orange"), "Parar", self.fonte)

        self.next_question(first=True)
        self.is_loaded = all(image is not None for image in self.images.values())

    def run(self, events):
        self.screen.fill("black")
        self.screen.blit(self.images["background"], (0, 0))

        for text in self.texts:
            text.draw(self.screen)

        level_str = f'Pergunta {self.len_questions - len(self.pool.questions) + 1} / {self.len_questions}'
        font = pygame.font.SysFont(None, 32)
        perg_text = font.render(level_str, True, pygame.Color("white"))
        self.screen.blit(perg_text, (WINDOW_SIZE[0] / 2 - perg_text.get_width() / 2, 50))

        self.score.draw(self.screen)
        self.meio_a_meio_btn.draw(self.screen)
        self.pular_btn.draw(self.screen)
        self.parar_btn.draw(self.screen)

        for answer_btn in self.answer_btn:
            answer_btn.draw(self.screen)
            if answer_btn.check_button():
                texto_resposta = answer_btn.text
                correta = self.pool.is_correct_answer(texto_resposta)
    
                if correta:
                    self.next_question(correct=True)
                else:
                    # Redireciona para a TelaErro
                    from Telas.TelaErro import TelaErro
                    pontuacao_visual = self.checkpoint * 100000
                    self.score.score = self.checkpoint
                    DATABASE.add_pontuacao_real(self.id_partida, self.checkpoint)
                    self.transition_call(TelaErro(self.screen, self.transition_call, pontuacao_visual, self.quit_game))
                    return 
            
        # Verifica clique no botão parar
        if self.parar_btn.check_button():
            self.encerrar_jogo()
            return      
        # DICA: Pular pergunta
        if self.pular_btn.check_click() and not self.usou_pular:
            print("PULAR clicado")  
            self.usou_pular = True
            DATABASE.usar_pular_dica(self.id_partida)
            self.next_question()

        # DICA: Meio a Meio
        if self.meio_a_meio_btn.check_click() and not self.usou_meio:
            print("MEIO A MEIO clicado")
            self.usou_meio = True
            DATABASE.usar_meio_a_meio(self.id_partida)

            corretas = [a for a in self.answers if a["correct"]]
            erradas = [a for a in self.answers if not a["correct"]]
            if len(erradas) >= 2:
                removidas = random.sample(erradas, 2)
                self.answers = corretas + [e for e in erradas if e not in removidas]

            self.answer_btn = []
            for idx, a in enumerate(self.answers):
                pos_y = WINDOW_SIZE[1] / 2 + 120 * idx / 2 + 50
                self.answer_btn.append(
                    Botao((50, pos_y), (700, 40), pygame.Color("gray"), a["text"], self.fonte)
                )


    def next_question(self, first=False, correct=False):
        if not first:
            if not self.ended and correct:
                self.acertos += 1
                self.score.increment_score()
            
            if self.acertos in [3, 7]:
                self.checkpoint = self.acertos
                print("Checkpoint atingido")

        if len(self.pool.questions) == 1:
            self.transition_call(TelaAcerto(self.screen, self.transition_call, self.quit_game))
            self.ended = True
            DATABASE.add_pontuacao_real(self.id_partida, self.acertos)

        else:
            if not first:
                self.pool.questions.pop(0)
                self.pool.next_question()

            self.text = self.pool.get_question()
            self.answers = self.pool.get_answers()  

            self.answer_btn = []
            for idx, a in enumerate(self.answers):
                pos_y = WINDOW_SIZE[1] / 2 + 120 * idx / 2 + 50
                self.answer_btn.append(
                    Botao((50, pos_y), (700, 40), pygame.Color("gray"), a["text"], self.fonte)
                )

            self.texts = break_line(
                self.text, pygame.Vector2(50, 100) 
            )
    
    def encerrar_jogo(self):
        # Salvar pontuação real (quantidade de acertos) no banco
        DATABASE.add_pontuacao_real(self.id_partida, self.acertos)
        from Telas.TelaInicio import TelaInicio
        self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game))
