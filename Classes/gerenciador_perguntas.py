class GerenciadorPerguntas:
    def __init__(self):
        self.perguntas = ["Pergunta Inicial 1", "Outra Pergunta"] # Exemplo inicial

    def adicionar_pergunta(self, texto_pergunta):
        self.perguntas.append(texto_pergunta)
        print(f"Pergunta '{texto_pergunta}' adicionada.")

    def listar_perguntas(self):
        return self.perguntas