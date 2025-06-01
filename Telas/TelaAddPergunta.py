import pygame
from interfaces.database import Database
db = Database()
 

class AddPerguntaTela:
    def __init__(self):
        self.db = Database()
        self.largura, self.altura = 1280, 720
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Adicionar Pergunta")

        self.margem = 20
        self.fonte_30 = pygame.font.Font(None, 30)
        self.fonte_24 = pygame.font.Font(None, 24)

        self.label_pergunta = self.fonte_30.render("PERGUNTA", True, pygame.Color("white"))
        self.rect_label = self.label_pergunta.get_rect(topleft=(self.margem, self.margem))

        self.caixatexto = pygame.Rect(self.margem, self.rect_label.bottom + 10, 400, 100)
        self.texto_pergunta = ""
        self.ativo_pergunta = False

        self.rects_alt = [pygame.Rect(self.margem, self.caixatexto.bottom + 20 + i * 50,
                                      self.caixatexto.width, 40) for i in range(4)]
        self.textos_alt = [""] * 4
        self.ativos_alt = [False] * 4

        bw, bh, esp = 120, 40, 10
        x_lat = self.largura - self.margem - bw
        self.rect_add = pygame.Rect(x_lat, self.margem, bw, bh)
        self.rect_cancel = pygame.Rect(x_lat, self.margem + bh + esp, bw, bh)

        # Filtros
        self.filtros_dif = ["Fácil", "Média", "Difícil"]
        self.filtros_mat = ["história", "matemática", "física", "química", "biologia",
                            "geometria", "português", "literatura"]

        self.rect_filt_dif = pygame.Rect(self.margem, self.altura - self.margem - 30, 120, 30)
        self.rect_filt_mat = pygame.Rect(self.rect_filt_dif.right + 10, self.altura - self.margem - 30, 140, 30)

        self.mostrar_dif = False
        self.mostrar_mat = False

        self.rect_box_dif = pygame.Rect(self.rect_filt_dif.x, self.rect_filt_dif.y - len(self.filtros_dif)*30 - 10,
                                        150, len(self.filtros_dif)*30 + 10)
        self.rect_box_mat = pygame.Rect(self.rect_filt_mat.x, self.rect_filt_mat.y - len(self.filtros_mat)*30 - 10,
                                        180, len(self.filtros_mat)*30 + 10)

        self.rects_filt_dif = [pygame.Rect(self.rect_box_dif.x + 5, self.rect_box_dif.y + 5 + i * 30,
                                           self.rect_box_dif.width - 10, 25) for i in range(len(self.filtros_dif))]
        self.rects_filt_mat = [pygame.Rect(self.rect_box_mat.x + 5, self.rect_box_mat.y + 5 + i * 30,
                                           self.rect_box_mat.width - 10, 25) for i in range(len(self.filtros_mat))]

        self.sel_dificuldade = None
        self.sel_materia = None

    def desenhar_texto_centralizado(self, texto, fonte, cor, rect):
        surf = fonte.render(texto, True, cor)
        texto_rect = surf.get_rect(center=rect.center)
        self.tela.blit(surf, texto_rect)

    def executar(self):
        rodando = True
        retorno = "cancelar"

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    retorno = "fechar_janela"

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Filtros - verifica se clicou nos botões principais
                    if self.rect_filt_dif.collidepoint(pos):
                        self.mostrar_dif = not self.mostrar_dif
                    elif self.rect_filt_mat.collidepoint(pos):
                        self.mostrar_mat = not self.mostrar_mat
                    
                    # Verifica se clicou nas opções dos filtros
                    if self.mostrar_dif:
                        for i, r in enumerate(self.rects_filt_dif):
                            if r.collidepoint(pos):
                                self.sel_dificuldade = self.filtros_dif[i]
                                # Não fecha o menu após selecionar
                                # self.mostrar_dif = False

                    if self.mostrar_mat:
                        for i, r in enumerate(self.rects_filt_mat):
                            if r.collidepoint(pos):
                                self.sel_materia = self.filtros_mat[i]
                                # Não fecha o menu após selecionar
                                # self.mostrar_mat = False

                    # Fecha os menus se clicar fora
                    if not (self.rect_filt_dif.collidepoint(pos) or 
                            self.rect_filt_mat.collidepoint(pos) or
                            any(r.collidepoint(pos) for r in self.rects_filt_dif) or
                            any(r.collidepoint(pos) for r in self.rects_filt_mat)):
                        # Mantém os menus abertos se já estiverem abertos
                        pass

                    # Caixa de texto e alternativas
                    if self.caixatexto.collidepoint(pos):
                        self.ativo_pergunta = True
                        self.ativos_alt = [False] * 4
                    else:
                        self.ativo_pergunta = False
                        for i, r in enumerate(self.rects_alt):
                            if r.collidepoint(pos):
                                self.ativos_alt = [False] * 4
                                self.ativos_alt[i] = True

                    # Botões
                    if self.rect_add.collidepoint(pos):
                        materias = {
                            "português": 1,
                            "química": 2,
                            # Adicione os outros conforme existirem no banco
                        }

                        if not self.texto_pergunta.strip() or not all(self.textos_alt):
                            print("Preencha a pergunta e todas as alternativas.")
                            continue

                        if not self.sel_dificuldade or not self.sel_materia:
                            print("Selecione uma dificuldade e uma matéria.")
                            continue

                        idMateria = materias[self.sel_materia]
                        try:
                            self.db.add_questao(
                                self.texto_pergunta.strip(), self.sel_dificuldade, idMateria,
                                self.textos_alt[0].strip(), self.textos_alt[1].strip(),
                                self.textos_alt[2].strip(), self.textos_alt[3].strip()
                            )
                            print("Pergunta adicionada com sucesso.")
                            rodando = False
                            retorno = "adicionada"
                        except Exception as e:
                            print("Erro ao adicionar pergunta:", e)

                    elif self.rect_cancel.collidepoint(pos):
                        rodando = False
                        retorno = "cancelar"

                elif evento.type == pygame.KEYDOWN:
                    if self.ativo_pergunta:
                        if evento.key == pygame.K_BACKSPACE:
                            self.texto_pergunta = self.texto_pergunta[:-1]
                        elif evento.key != pygame.K_RETURN:
                            self.texto_pergunta += evento.unicode
                    else:
                        for i, ativo in enumerate(self.ativos_alt):
                            if ativo:
                                if evento.key == pygame.K_BACKSPACE:
                                    self.textos_alt[i] = self.textos_alt[i][:-1]
                                elif evento.key != pygame.K_RETURN:
                                    self.textos_alt[i] += evento.unicode

            # DESENHO
            self.tela.fill(pygame.Color("lightgrey"))
            self.tela.blit(self.label_pergunta, self.rect_label)

            cor_bg = pygame.Color("dimgray")
            cor_border = pygame.Color("dodgerblue") if self.ativo_pergunta else pygame.Color("gray")
            self.tela.fill(cor_bg, self.caixatexto)
            pygame.draw.rect(self.tela, cor_border, self.caixatexto, 2, border_radius=5)
            surf = self.fonte_30.render(self.texto_pergunta, True, pygame.Color("white"))
            self.tela.blit(surf, (self.caixatexto.x + 5, self.caixatexto.y + 5))

            for i, r in enumerate(self.rects_alt):
                cor_b = pygame.Color("dodgerblue") if self.ativos_alt[i] else pygame.Color("gray")
                self.tela.fill(cor_bg, r)
                pygame.draw.rect(self.tela, cor_b, r, 2, border_radius=5)
                rot = self.fonte_24.render(f"{chr(65 + i)}.", True, pygame.Color("white"))
                self.tela.blit(rot, (r.x - 30, r.y + 5))
                text = self.fonte_30.render(self.textos_alt[i], True, pygame.Color("white"))
                self.tela.blit(text, (r.x + 10, r.y + 5))

            for rect, txt in [(self.rect_add, "ADICIONAR"),
                              (self.rect_cancel, "CANCELAR"),
                              (self.rect_filt_dif, "DIFICULDADE"),
                              (self.rect_filt_mat, "MATÉRIA")]:
                cor_btn = pygame.Color("saddlebrown")
                self.tela.fill(cor_btn, rect)
                self.desenhar_texto_centralizado(txt, self.fonte_24, pygame.Color("white"), rect)

            # Desenha os filtros de dificuldade
            if self.mostrar_dif:
                self.tela.fill(pygame.Color("gray20"), self.rect_box_dif)
                pygame.draw.rect(self.tela, pygame.Color("gray"), self.rect_box_dif, 2, border_radius=5)
                for i, (f, r) in enumerate(zip(self.filtros_dif, self.rects_filt_dif)):
                    # Verde para selecionado, vermelho para não selecionado
                    cor = pygame.Color("green") if f == self.sel_dificuldade else pygame.Color("red")
                    self.tela.fill(cor, r)
                    text = self.fonte_24.render(f, True, pygame.Color("white"))
                    self.tela.blit(text, (r.x + 5, r.y + 5))

            # Desenha os filtros de matéria
            if self.mostrar_mat:
                self.tela.fill(pygame.Color("gray20"), self.rect_box_mat)
                pygame.draw.rect(self.tela, pygame.Color("gray"), self.rect_box_mat, 2, border_radius=5)
                for i, (f, r) in enumerate(zip(self.filtros_mat, self.rects_filt_mat)):
                    # Verde para selecionado, vermelho para não selecionado
                    cor = pygame.Color("green") if f == self.sel_materia else pygame.Color("red")
                    self.tela.fill(cor, r)
                    text = self.fonte_24.render(f, True, pygame.Color("white"))
                    self.tela.blit(text, (r.x + 5, r.y + 5))

            pygame.display.flip()

        return retorno


if __name__ == '__main__':
    pygame.init()
    app = AddPerguntaTela()
    app.executar()
    pygame.quit()