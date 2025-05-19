# Classes/TelaPrincipal.py
import pygame
import sys
from Classes.elementos_visuais import Cores, escalar, escalar_y
from Classes.componentes import Botao, Alternativa

class TelaPrincipal:
    def __init__(self, resolucao_original=(1920, 1080), resolucao_desejada=(1280, 720)):
        pygame.init()
        self.resolucao_original_x = resolucao_original[0]
        self.resolucao_original_y = resolucao_original[1]
        self.resolucao_desejada_x = resolucao_desejada[0]
        self.resolucao_desejada_y = resolucao_desejada[1]
        self.screen = pygame.display.set_mode((self.resolucao_desejada_x, self.resolucao_desejada_y))
        pygame.display.set_caption("Quiz com Fundo Imagem")

        self.background = pygame.transform.scale(pygame.image.load("imagens/Prancheta 2.png"), (self.resolucao_desejada_x, self.resolucao_desejada_y))

        self.font_question = pygame.font.SysFont('Arial', escalar(48, self.resolucao_original_x, self.resolucao_desejada_x))
        self.font_alternative = pygame.font.SysFont('Arial', escalar(36, self.resolucao_original_x, self.resolucao_desejada_x))
        self.font_button = pygame.font.SysFont('Arial', escalar(40, self.resolucao_original_x, self.resolucao_desejada_x))
        self.font_acerto = pygame.font.SysFont('Arial', escalar(120, self.resolucao_original_x, self.resolucao_desejada_x), bold=True)

        self.botao_premio_rect = pygame.Rect(escalar(1500, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(0, self.resolucao_original_y, self.resolucao_desejada_y), escalar(250, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(80, self.resolucao_original_y, self.resolucao_desejada_y))
        self.area_premio = pygame.Rect(escalar(500, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(700, self.resolucao_original_y, self.resolucao_desejada_y), escalar(200, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(60, self.resolucao_original_y, self.resolucao_desejada_y))
        self.area_pergunta = pygame.Rect(escalar(80, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(70, self.resolucao_original_y, self.resolucao_desejada_y), escalar(1400, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(150, self.resolucao_original_y, self.resolucao_desejada_y))

        self.alternativas_dict = {"A": "Rio de Janeiro", "B": "São Paulo", "C": "Brasília", "D": "Minas gerais"}
        self.areas_alternativas = self._criar_areas_alternativas()
        self.alternativas_objetos = self._criar_objetos_alternativas()

        self.btn_confirmar = Botao(pygame.Rect(escalar(200, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(1010, self.resolucao_original_y, self.resolucao_desejada_y), escalar(200, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(60, self.resolucao_original_y, self.resolucao_desejada_y)), "Confirmar", self.font_button)
        self.btn_parar = Botao(pygame.Rect(escalar(550, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(1010, self.resolucao_original_y, self.resolucao_desejada_y), escalar(200, self.resolucao_original_x, self.resolucao_desejada_x), escalar_y(60, self.resolucao_original_y, self.resolucao_desejada_y)), "Parar", self.font_button)

        self.pergunta = "Qual a capital do brasil?."
        self.alternativa_selecionada = None
        self.mostrar_acerto = False
        self.running = True

    def _escalar(self, valor):
        return escalar(valor, self.resolucao_original_x, self.resolucao_desejada_x)

    def _escalar_y(self, valor):
        return escalar_y(valor, self.resolucao_original_y, self.resolucao_desejada_y)

    def _criar_areas_alternativas(self):
        areas = {}
        y_offset_inicial = self._escalar_y(380)
        altura_alternativa = self._escalar_y(100)
        espacamento_vertical = self._escalar_y(70)
        for chave, texto in self.alternativas_dict.items():
            posicao_y = y_offset_inicial + (list(self.alternativas_dict.keys()).index(chave)) * (altura_alternativa + espacamento_vertical)
            areas[chave] = pygame.Rect(self._escalar(50), posicao_y, self._escalar(900), altura_alternativa)
        return areas

    def _criar_objetos_alternativas(self):
        alternativas = {}
        for chave, texto in self.alternativas_dict.items():
            alternativas[chave] = Alternativa(self.areas_alternativas[chave], f"{chave}) {texto}", self.font_alternative)
        return alternativas

    def desenhar_texto_quebrado(self, surface, texto, font, color, rect):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ''
        for palavra in palavras:
            teste_linha = linha_atual + palavra + ' '
            texto_teste = font.render(teste_linha, True, color)
            if texto_teste.get_width() < rect.width:
                linha_atual = teste_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + ' '
        linhas.append(linha_atual)

        y_offset = rect.top
        espacamento_linhas = self._escalar_y(10)
        for linha in linhas:
            texto_renderizado = font.render(linha.strip(), True, color)
            texto_rect = texto_renderizado.get_rect(topleft=(rect.left, y_offset))
            surface.blit(texto_renderizado, texto_rect)
            y_offset += texto_renderizado.get_height() + espacamento_linhas

    def desenhar_botao_premio(self, surface, rect, texto, fonte, cor_texto, cor_fundo, cor_borda):
        pygame.draw.rect(surface, cor_borda, rect)
        inner_rect = rect.inflate(-self._escalar(16), -self._escalar_y(16))
        pygame.draw.rect(surface, cor_fundo, inner_rect)
        text_surf = fonte.render(texto, True, cor_texto)
        text_rect = text_surf.get_rect(center=inner_rect.center)
        surface.blit(text_surf, text_rect)

    def executar(self):
        while self.running:
            self.screen.blit(self.background, (0, 0))
            self.desenhar_texto_quebrado(self.screen, self.pergunta, self.font_question, Cores.WHITE, self.area_pergunta)
            self.desenhar_botao_premio(self.screen, self.botao_premio_rect, "PRÊMIO", self.font_button, Cores.WHITE, Cores.RED, Cores.BLACK)

            mouse_pos = pygame.mouse.get_pos()

            for alternativa in self.alternativas_objetos.values():
                alternativa.verificar_hover(mouse_pos)
                alternativa.desenhar(self.screen)

            self.btn_confirmar.verificar_hover(mouse_pos)
            self.btn_confirmar.desenhar(self.screen)
            self.btn_parar.verificar_hover(mouse_pos)
            self.btn_parar.desenhar(self.screen)

            if self.mostrar_acerto:
                texto_acerto = self.font_acerto.render("ACERTOU!!!", True, Cores.BLUE)
                texto_acerto_rect = texto_acerto.get_rect(center=self.screen.get_rect().center)
                self.screen.blit(texto_acerto, texto_acerto_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for chave, alternativa_obj in self.alternativas_objetos.items():
                        if alternativa_obj.verificar_clique(event):
                            self.alternativa_selecionada = chave
                            for alt in self.alternativas_objetos.values():
                                alt.selecionada = (alt is alternativa_obj)
                            print(f"Alternativa selecionada: {chave} - {self.alternativas_dict[chave]}")
                            break

                    if self.btn_confirmar.verificar_clique(event):
                        print("Botão Confirmar clicado!")
                        if self.alternativa_selecionada is not None:
                            print(f"Confirmando alternativa: {self.alternativa_selecionada} - {self.alternativas_dict[self.alternativa_selecionada]}")
                            self.mostrar_acerto = True # Lógica de verificação da resposta real viria aqui
                        else:
                            print("Nenhuma alternativa selecionada!")

                    elif self.btn_parar.verificar_clique(event):
                        print("Botão Parar clicado!")
                        self.running = False

                    elif self.botao_premio_rect.collidepoint(event.pos):
                        print("Botão PRÊMIO clicado!")
                        # Adicionar ação do botão prêmio

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    tela_principal = TelaPrincipal()
    tela_principal.executar()