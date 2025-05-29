import pygame
from Telas.Tela import Tela
from UI.Botao import Botao
from interfaces.database import Database

db = Database()
db.connect()  # Certifique-se de que sua classe aceita o parâmetro

class TelaAddAluno(Tela):
    def __init__(self, screen, transition_call, largura=1280, altura=720):
        super().__init__(screen, transition_call)
        self.largura = largura
        self.altura = altura
        self.tela = pygame.Surface((largura, altura))
        pygame.display.set_caption("Adicionar Aluno")

        self.fonte = pygame.font.Font(None, 16)

        self.caixas = [
            self._criar_caixa_texto(20, 50, "NOME"),
            self._criar_caixa_texto(20, 120, "EMAIL"),
            self._criar_caixa_texto(20, 190, "SENHA")
        ]

        self.botao_add = Botao((290, 50), (120, 40), pygame.Color("saddlebrown"), "ADICIONAR", self.fonte)
        self.botao_cancel = Botao((290, 120), (120, 40), pygame.Color("saddlebrown"), "CANCELAR", self.fonte)

        self.retorno = "cancelar"
        self.rodando = True

    def _criar_caixa_texto(self, x, y, label):
        rect = pygame.Rect(x, y, 250, 40)
        return {"rect": rect, "texto": "", "label": label, "ativo": False}

    def _desenhar_caixa_texto(self, tela, caixa):
        pygame.draw.rect(tela, pygame.Color("dimgray"), caixa["rect"], border_radius=5)
        cor_borda = pygame.Color("dodgerblue") if caixa["ativo"] else pygame.Color("gray")
        pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=5)

        label = pygame.font.Font(None, 24).render(caixa["label"], True, pygame.Color("white"))
        tela.blit(label, (caixa["rect"].x, caixa["rect"].y - 20))

        texto = self.fonte.render(caixa["texto"], True, pygame.Color("white"))
        tela.blit(texto, (caixa["rect"].x + 5, caixa["rect"].y + 8))

    def executar(self, tela_principal):
        while self.rodando:
            self.tela.fill(pygame.Color("lightgray"))

            for caixa in self.caixas:
                self._desenhar_caixa_texto(self.tela, caixa)

            self.botao_add.draw(self.tela)
            self.botao_cancel.draw(self.tela)

            tela_principal.blit(self.tela, (0, 0))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.retorno = "fechar_janela"
                    self.rodando = False

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for caixa in self.caixas:
                        caixa["ativo"] = caixa["rect"].collidepoint(pos)

                elif evento.type == pygame.KEYDOWN:
                    for caixa in self.caixas:
                        if caixa["ativo"]:
                            if evento.key == pygame.K_BACKSPACE:
                                caixa["texto"] = caixa["texto"][:-1]
                            elif evento.key != pygame.K_RETURN:
                                caixa["texto"] += evento.unicode

            if self.botao_add.check_button():
                nome = self.caixas[0]["texto"].strip()
                email = self.caixas[1]["texto"].strip()
                senha = self.caixas[2]["texto"].strip()

                if nome and email and senha:
                    sucesso = db.add_aluno(nome, email, senha)  # <-- usa sua função aqui!
                    if sucesso:
                        self.retorno = "aluno_adicionado"
                    else:
                        self.retorno = "erro"
                    self.rodando = False
                else:
                    print("Preencha todos os campos.")

            elif self.botao_cancel.check_button():
                self.retorno = "cancelar"
                self.rodando = False

        return self.retorno
