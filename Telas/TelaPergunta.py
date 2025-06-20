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
    def __init__(self, screen, transition_call, id_materia, quit_game, id_partida , id_aluno):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.ended = False
        self.acertos = 0
        self.images = {}
        self.texts = []
        self.answer_btn = []
        self.id_materia = id_materia
        self.id_partida = id_partida
        self.id_aluno = id_aluno
        self.quit_game = quit_game
        self.checkpoint = 0  # valor salvo ao atingir o checkpoint
        self.pergunta_atual = 1
        self.fonte = pygame.font.SysFont("Arial", 25)
        self.resposta_errada_marcada = False
        self.botao_resposta_certa = None
        self.botao_resposta_errada = None
        self.tempo_erro = None

        # Verifica se já existe entrada na tabela Dica para essa partida
        dica_existente = DATABASE.get_dica_por_partida(self.id_partida)
        if not dica_existente:
            DATABASE.criar_dica_para_partida(self.id_partida)

        # Flags locais de uso (evita múltiplos cliques)
        self.usou_meio = dica_existente["MeioaMeio"] if dica_existente else False
        self.usou_pular = dica_existente["PularDica"] if dica_existente else False

    def load(self):
        perguntas_faceis = json.loads(DATABASE.get_questoes_por_materia_e_dificuldade_json(self.id_materia, "Fácil"))
        perguntas_medias = json.loads(DATABASE.get_questoes_por_materia_e_dificuldade_json(self.id_materia, "Média"))
        perguntas_dificeis = json.loads(DATABASE.get_questoes_por_materia_e_dificuldade_json(self.id_materia, "Difícil"))
        random.shuffle(perguntas_faceis)
        random.shuffle(perguntas_medias)
        random.shuffle(perguntas_dificeis)
        selected_questions = perguntas_faceis[:4] + perguntas_medias[:4] + perguntas_dificeis[:2]
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

        for btn in self.answer_btn:
            if self.resposta_errada_marcada:
                if btn == self.botao_resposta_errada:
                    btn.color = pygame.Color("red")
                elif btn == self.botao_resposta_certa:
                    btn.color = pygame.Color("green")
                else:
                    btn.color = pygame.Color("gray")
            btn.draw(self.screen)

    # Verificação de clique apenas se ainda não errou
        if not self.resposta_errada_marcada:
            for btn in self.answer_btn:
                if btn.check_button():
                    texto_resposta = btn.text
                    if self.pool.is_correct_answer(texto_resposta):
                        self.next_question(correct=True)
                    else:
                        self.resposta_errada_marcada = True
                        self.botao_resposta_errada = btn
                        for b in self.answer_btn:
                            if self.pool.is_correct_answer(b.text):
                                self.botao_resposta_certa = b
                                break
                        self.tempo_erro = pygame.time.get_ticks()
                        DATABASE.add_pontuacao_real(self.id_partida, self.acertos)

   
        if self.resposta_errada_marcada and self.tempo_erro:
            if pygame.time.get_ticks() - self.tempo_erro > 3000:
                from Telas.TelaErro import TelaErro
                pontuacao_visual = self.checkpoint * 100000
                self.score.score = self.checkpoint
                self.transition_call(TelaErro(self.screen, self.transition_call, pontuacao_visual, self.quit_game, self.id_aluno))
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
            self.transition_call(TelaAcerto(self.screen, self.transition_call, self.quit_game, self.id_aluno))
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
        self.transition_call(TelaInicio(self.screen, self.transition_call, self.quit_game, user_data={"tipo":"Aluno", "id": self.id_aluno}))
