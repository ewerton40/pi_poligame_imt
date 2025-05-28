import random

class Pergunta:
    def __init__(self, questions: list[dict]):
        print(questions)
        self.questions = questions
        self.index = 0
        self.current_question = 0

    def get_question(self) -> str:
        if len(self.questions) == 0:
            return "No questions left"

        return self.questions[self.current_question]["question"]

    def get_questions(self) -> list[dict]:
        return self.questions

    def next_question(self) -> None:
        self.current_question = 0

    def get_answers(self) -> list[dict]:
        if len(self.questions) == 0:
            return []

        shuffled = self.questions[self.current_question]["answers"]
        random.shuffle(shuffled)

        return shuffled

    def is_correct_answer(self, guess:str) -> bool:
        for a in self.questions[self.current_question]["answers"]:
            if a["text"] == guess:
                return True if a["correct"] == 1 else False
        return False

    def get_id_pergunta_atual(self):
        return self.questions[self.index]["id"]

    def get_id_resposta_por_texto(self, texto):
        for resposta in self.questions[self.index]["answers"]:
            if resposta["text"] == texto:
                return resposta["id"]
        return None
