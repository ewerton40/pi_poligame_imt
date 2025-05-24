import pygame

class UIComponentes:
    @staticmethod
    def desenhar_texto_centralizado(tela, texto, tamanho_fonte, cor, rect):
        fonte = pygame.font.Font(None, tamanho_fonte)
        texto_renderizado = fonte.render(texto, True, cor)
        texto_rect = texto_renderizado.get_rect(center=rect.center)
        tela.blit(texto_renderizado, texto_rect)

    @staticmethod
    def criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
        rect = pygame.Rect(x, y, largura, altura)
        return {"rect": rect, "texto": texto_inicial, "label": texto_label, "ativo": False}

    @staticmethod
    def desenhar_caixa_texto(tela, caixa):
        cor_fundo = pygame.Color("dimgray")
        cor_borda = pygame.Color("dodgerblue") if caixa["ativo"] else pygame.Color("gray")
        cor_texto = pygame.Color("white")

        pygame.draw.rect(tela, cor_fundo, caixa["rect"], 0, border_radius=10)
        pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=10)

        fonte_texto = pygame.font.Font(None, 30)
        texto_surf = fonte_texto.render(caixa["texto"], True, cor_texto)
        tela.blit(
            texto_surf,
            (
                caixa["rect"].x + 10,
                caixa["rect"].y + (caixa["rect"].height - texto_surf.get_height()) // 2
            )
        )

        fonte_label = pygame.font.Font(None, 24)
        label_surf = fonte_label.render(caixa["label"], True, cor_texto)
        tela.blit(
            label_surf,
            (
                caixa["rect"].x + 10,
                caixa["rect"].y - label_surf.get_height() - 5
            )
        )

    @staticmethod
    def criar_botao(texto, x, y, largura, altura):
        rect = pygame.Rect(x, y, largura, altura)
        return {"rect": rect, "texto": texto}

    @staticmethod
    def desenhar_botao(tela, botao):
        cor_botao = pygame.Color("dimgray")
        cor_texto = pygame.Color("white")

        pygame.draw.rect(tela, cor_botao, botao["rect"], 0, border_radius=10)
        UIComponentes.desenhar_texto_centralizado(tela, botao["texto"], 24, cor_texto, botao["rect"])
        return botao["rect"]
