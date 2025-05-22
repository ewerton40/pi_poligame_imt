import pygame

# Fontes locais
FONTE_PADRAO = pygame.font.Font(None, 30)
FONTE_PEQUENA = pygame.font.Font(None, 24)

# Desenha texto centralizado
def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    surf = fonte.render(texto, True, cor)
    texto_rect = surf.get_rect(center=rect.center)
    tela.blit(surf, texto_rect)

# Cria caixas de texto
def criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto_inicial, "label": texto_label, "ativo": False}

# Desenha caixa de texto com label
def desenhar_caixa_texto(tela, caixa):
    cor_fundo = pygame.Color("dimgray")
    cor_borda = pygame.Color("dodgerblue") if caixa["ativo"] else pygame.Color("gray")
    cor_texto = pygame.Color("white")

    # Fundo e borda
    pygame.draw.rect(tela, cor_fundo, caixa["rect"], 0, border_radius=5)
    pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=5)

    # Label
    if caixa.get("label"):
        label_surf = FONTE_PEQUENA.render(caixa["label"], True, cor_texto)
        tela.blit(label_surf, (caixa["rect"].x, caixa["rect"].y - label_surf.get_height() - 5))

    # Texto digitado
    texto_surf = FONTE_PADRAO.render(caixa["texto"], True, cor_texto)
    tela.blit(
        texto_surf,
        (
            caixa["rect"].x + 5,
            caixa["rect"].y + (caixa["rect"].height - texto_surf.get_height()) // 2
        )
    )

# Cria botão simples
def criar_botao(texto, x, y, largura, altura):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto}

# Desenha botão com texto centrado
def desenhar_botao(tela, botao):
    cor_btn = pygame.Color("saddlebrown")
    cor_txt = pygame.Color("white")
    pygame.draw.rect(tela, cor_btn, botao["rect"], 0, border_radius=5)
    desenhar_texto_centralizado(tela, botao["texto"], FONTE_PADRAO, cor_txt, botao["rect"])
    return botao["rect"]

# Função principal para adicionar aluno
def abrir_tela_adicionar_aluno(tela_principal):
    largura, altura = 800, 600
    tela = pygame.Surface((largura, altura))
    pygame.display.set_caption("Adicionar Aluno")

    # Caixas de input
    caixa_email = criar_caixa_texto(20, 50, 250, 40, texto_label="EMAIL")
    caixa_senha = criar_caixa_texto(20, 120, 250, 40, texto_label="SENHA")
    caixas = [caixa_email, caixa_senha]

    # Botões
    rect_add = criar_botao("ADICIONAR", 290, 50, 120, 40)
    rect_cancel = criar_botao("CANCELAR", 290, 120, 120, 40)
    botoes = [rect_add, rect_cancel]

    rodando = True
    retorno = "cancelar"

    while rodando:
        # Desenho de fundo
        tela.fill(pygame.Color("lightgray"))

        # Desenha caixas e botões
        for caixa in caixas:
            desenhar_caixa_texto(tela, caixa)
        for botao in botoes:
            desenhar_botao(tela, botao)

        # Exibe na tela principal
        tela_principal.blit(tela, (0, 0))
        pygame.display.flip()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "fechar_janela"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Ativa caixas conforme clique
                for caixa in caixas:
                    caixa["ativo"] = caixa["rect"].collidepoint(pos)
                # Botões
                if botoes[0]["rect"].collidepoint(pos):
                    email = caixa_email["texto"]
                    senha = caixa_senha["texto"]
                    print(f"Adicionar Aluno - Email: {email}, Senha: {senha}")
                    retorno = "adicionar_aluno"
                    rodando = False
                elif botoes[1]["rect"].collidepoint(pos):
                    retorno = "cancelar"
                    rodando = False

            if evento.type == pygame.KEYDOWN:
                for caixa in caixas:
                    if caixa["ativo"]:
                        if evento.key == pygame.K_BACKSPACE:
                            caixa["texto"] = caixa["texto"][:-1]
                        elif evento.key != pygame.K_RETURN:
                            caixa["texto"] += evento.unicode

    return retorno

if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((800, 600))
    resultado = abrir_tela_adicionar_aluno(tela_teste)
    print(f"Resultado: {resultado}")
    pygame.quit()
