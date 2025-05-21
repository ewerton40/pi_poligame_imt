import pygame
import json
import random
from UI.Botao import Botao
from UI.Pontuacao import Pontuacao
import Pergunta # Classe que gerencia perguntas
from util import WINDOW_SIZE, break_line, DATABASE, USER

class TelaPergunta(Tela):
    def __init__(self, screen, transition_call):
        super().__init__(screen, transition_call)
        self.screen = screen
        self.ended = False
        self.images = {}
        self.texts = []
        self.answer_btn = []

    def load(self):
        questions = DATABASE.get_all_questions_json()
        perguntas = json.loads(questions)
        random.shuffle(perguntas)
        selected_questions = perguntas[:10]
        #Cria um pool de perguntas
        self.pool = Pergunta(selected_questions)
        self.text = self.pool.get_question() #Pega a primeira pergunta
        self.answers:list[dict] = self.pool.get_answers() #Pega as respostas para compará-las com a pergunta
        self.score = Pontuacao((1170, 10), (100, 50), pygame.Color("red"))
        self.len_questions = len(self.pool.questions) 

        self.images = {
            "background": pygame.image.load("imagens/imagem_pergunta.jpeg").convert_alpha(),
        }

        self.next_question(first=True)
        self.is_loaded = all(image is not None for image in self.images.values())

    def run(self):
        self.screen.fill("black")
        self.screen.blit(self.images["background"], (0, 0))

        for text in self.texts:
            text.draw(self.screen)

        level_str = f'Level {self.len_questions - len(self.pool.questions) + 1} / {self.len_questions}'
        font = pygame.font.Font("resources/fonts/monogram.ttf", 32)
        level_text = font.render(level_str, True, pygame.Color("gray"))
        self.screen.blit(level_text, (WINDOW_SIZE[0] / 2 - level_text.get_width() / 2, 35))

        self.score.draw(self.screen)

        for answer_btn in self.answer_btn:
            answer_btn.draw(self.screen)
            if answer_btn.check_button():
                if self.pool.is_correct_answer(answer_btn.text):
                    self.next_question(correct=True)
                else:
                    self.next_question()

    def next_question(self, first=False, correct=False):
        if not first:
            if not self.ended and correct:
                self.score.increment_score()

        if len(self.pool.questions) == 1:
            self.transition_call(TelaAcerto(self.screen, self.transition_call, self.score.score))
            self.ended = True
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
                    Botao((50, pos_y), (700, 40), pygame.Color("gray"), a["text"])
                )

            self.texts = break_line(
                self.text, pygame.Vector2(50, 40)
            )
