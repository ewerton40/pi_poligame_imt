import pygame

class AddPerguntaTela:
    def __init__(self):
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

        self.rect_filt = pygame.Rect(self.margem, self.altura - self.margem - 30, 100, 30)
        self.filtros = ["fácil", "médio", "difícil", "história", "matemática", "física", "química",
                        "biologia", "geometria", "português", "literatura"]
        self.sel_filtros = []
        self.mostrar = False
        self.rect_box = pygame.Rect(self.rect_filt.x, self.rect_filt.y - len(self.filtros) * 30 - 10,
                                    200, len(self.filtros) * 30 + 10)
        self.rects_filt = [pygame.Rect(self.rect_box.x + 5, self.rect_box.y + 5 + i * 30,
                                       self.rect_box.width - 10, 25) for i in range(len(self.filtros))]

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
                    if self.mostrar and not self.rect_box.collidepoint(pos):
                        self.mostrar = False
                    if self.rect_filt.collidepoint(pos):
                        self.mostrar = not self.mostrar

                    if self.caixatexto.collidepoint(pos):
                        self.ativo_pergunta = True
                        self.ativos_alt = [False] * 4
                    else:
                        self.ativo_pergunta = False
                        for i, r in enumerate(self.rects_alt):
                            if r.collidepoint(pos):
                                self.ativos_alt = [False] * 4
                                self.ativos_alt[i] = True
                                break

                    if self.rect_add.collidepoint(pos):
                        print("Adicionar:", self.texto_pergunta, self.textos_alt, self.sel_filtros)
                    elif self.rect_cancel.collidepoint(pos):
                        rodando = False
                        retorno = "cancelar"

                    if self.mostrar:
                        for i, r in enumerate(self.rects_filt):
                            if r.collidepoint(pos):
                                f = self.filtros[i]
                                if f in self.sel_filtros:
                                    self.sel_filtros.remove(f)
                                else:
                                    self.sel_filtros.append(f)

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

            # Desenho
            self.tela.fill(pygame.Color("black"))
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
                              (self.rect_filt, "FILTROS")]:
                cor_btn = pygame.Color("saddlebrown")
                self.tela.fill(cor_btn, rect)
                self.desenhar_texto_centralizado(txt, self.fonte_24, pygame.Color("white"), rect)

            if self.mostrar:
                self.tela.fill(cor_bg, self.rect_box)
                pygame.draw.rect(self.tela, pygame.Color("gray"), self.rect_box, 2, border_radius=5)
                for i, (f, r) in enumerate(zip(self.filtros, self.rects_filt)):
                    bg = pygame.Color("green") if f in self.sel_filtros else pygame.Color("red")
                    self.tela.fill(bg, r)
                    text = self.fonte_24.render(f, True, pygame.Color("white"))
                    self.tela.blit(text, (r.x + 5, r.y + 5))

            pygame.display.flip()

        return retorno


if __name__ == '__main__':
    pygame.init()
    tela_principal = pygame.display.set_mode((400, 300))
    app = AddPerguntaTela()
    resultado = app.executar()
    print("Resultado:", resultado)
    pygame.quit()
