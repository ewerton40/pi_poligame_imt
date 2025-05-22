import pygame

# Fontes
FONTE_PADRAO = pygame.font.Font(None, 30)
FONTE_PEQUENA = pygame.font.Font(None, 24)

# Função auxiliar para desenhar texto centralizado
def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    tela.blit(texto_renderizado, texto_rect)


def criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto_inicial, "label": texto_label, "ativo": False}


def desenhar_caixa_texto(tela, caixa):
    # cores inline na caixa de texto
    cor_fundo = pygame.Color("dimgray")
    cor_borda = pygame.Color("dodgerblue") if caixa["ativo"] else pygame.Color("gray")
    cor_texto = pygame.Color("white")

    pygame.draw.rect(tela, cor_fundo, caixa["rect"], 0, border_radius=10)
    pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=10)

    texto_surf = FONTE_PADRAO.render(caixa["texto"], True, cor_texto)
    tela.blit(
        texto_surf,
        (
            caixa["rect"].x + 10,
            caixa["rect"].y + (caixa["rect"].height - texto_surf.get_height()) // 2
        )
    )

    label_surf = FONTE_PEQUENA.render(caixa["label"], True, cor_texto)
    tela.blit(
        label_surf,
        (
            caixa["rect"].x + 10,
            caixa["rect"].y - label_surf.get_height() - 5
        )
    )


def criar_botao(texto, x, y, largura, altura):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto}


def desenhar_botao(tela, botao):
    # cores inline para cada botão
    cor_botao = pygame.Color("dimgray")
    cor_texto = pygame.Color("white")

    pygame.draw.rect(tela, cor_botao, botao["rect"], 0, border_radius=10)
    desenhar_texto_centralizado(tela, botao["texto"], FONTE_PEQUENA, cor_texto, botao["rect"])
    return botao["rect"]
