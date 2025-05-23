import pygame

class TelaAddAluno:
    def __init__(self, largura=800, altura=600):
        self.largura = largura
        self.altura = altura
        self.tela = pygame.Surface((self.largura, self.altura))
        pygame.display.set_caption("Adicionar Aluno")

        # Caixas de input
        self.caixa_email = self._criar_caixa_texto(20, 50, 250, 40, texto_label="EMAIL")
        self.caixa_senha = self._criar_caixa_texto(20, 120, 250, 40, texto_label="SENHA")
        self.caixas = [self.caixa_email, self.caixa_senha]

        # Botões
        self.botao_add = self._criar_botao("ADICIONAR", 290, 50, 120, 40)
        self.botao_cancel = self._criar_botao("CANCELAR", 290, 120, 120, 40)
        self.botoes = [self.botao_add, self.botao_cancel]

        self.retorno = "cancelar"
        self.rodando = True

    @staticmethod
    def _desenhar_texto_centralizado(tela, texto, tamanho_fonte, cor, rect):
        fonte = pygame.font.Font(None, tamanho_fonte)
        surf = fonte.render(texto, True, cor)
        texto_rect = surf.get_rect(center=rect.center)
        tela.blit(surf, texto_rect)

    @staticmethod
    def _criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
        rect = pygame.Rect(x, y, largura, altura)
        return {"rect": rect, "texto": texto_inicial, "label": texto_label, "ativo": False}

    @staticmethod
    def _desenhar_caixa_texto(tela, caixa):
        cor_fundo = pygame.Color("dimgray")
        cor_borda = pygame.Color("dodgerblue") if caixa["ativo"] else pygame.Color("gray")
        cor_texto = pygame.Color("white")

        pygame.draw.rect(tela, cor_fundo, caixa["rect"], 0, border_radius=5)
        pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=5)

        if caixa.get("label"):
            fonte_pequena = pygame.font.Font(None, 24)
            label_surf = fonte_pequena.render(caixa["label"], True, cor_texto)
            tela.blit(label_surf, (caixa["rect"].x, caixa["rect"].y - label_surf.get_height() - 5))

        fonte_padrao = pygame.font.Font(None, 30)
        texto_surf = fonte_padrao.render(caixa["texto"], True, cor_texto)
        tela.blit(
            texto_surf,
            (
                caixa["rect"].x + 5,
                caixa["rect"].y + (caixa["rect"].height - texto_surf.get_height()) // 2
            )
        )

    @staticmethod
    def _criar_botao(texto, x, y, largura, altura):
        rect = pygame.Rect(x, y, largura, altura)
        return {"rect": rect, "texto": texto}

    def _desenhar_botao(self, tela, botao):
        cor_btn = pygame.Color("saddlebrown")
        cor_txt = pygame.Color("white")
        pygame.draw.rect(tela, cor_btn, botao["rect"], 0, border_radius=5)
        self._desenhar_texto_centralizado(tela, botao["texto"], 30, cor_txt, botao["rect"])
        return botao["rect"]

    def executar(self, tela_principal):
        while self.rodando:
            self.tela.fill(pygame.Color("lightgray"))

            for caixa in self.caixas:
                self._desenhar_caixa_texto(self.tela, caixa)
            for botao in self.botoes:
                self._desenhar_botao(self.tela, botao)

            tela_principal.blit(self.tela, (0, 0))
            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                    self.retorno = "fechar_janela"

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for caixa in self.caixas:
                        caixa["ativo"] = caixa["rect"].collidepoint(pos)

                    if self.botao_add["rect"].collidepoint(pos):
                        email = self.caixa_email["texto"]
                        senha = self.caixa_senha["texto"]
                        print(f"Adicionar Aluno - Email: {email}, Senha: {senha}")
                        self.retorno = "adicionar_aluno"
                        self.rodando = False
                    elif self.botao_cancel["rect"].collidepoint(pos):
                        self.retorno = "cancelar"
                        self.rodando = False

                elif evento.type == pygame.KEYDOWN:
                    for caixa in self.caixas:
                        if caixa["ativo"]:
                            if evento.key == pygame.K_BACKSPACE:
                                caixa["texto"] = caixa["texto"][:-1]
                            elif evento.key != pygame.K_RETURN:
                                caixa["texto"] += evento.unicode
        return self.retorno


if __name__ == '__main__':
    pygame.init()
    tela_principal = pygame.display.set_mode((800, 600))
    tela_adicionar = TelaAddAluno()
    resultado = tela_adicionar.executar(tela_principal)
    print(f"Resultado: {resultado}")
    pygame.quit()
