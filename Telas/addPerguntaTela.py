import pygame

# Fontes locais
FONTE_PADRAO = pygame.font.Font(None, 30)
FONTE_PEQUENA = pygame.font.Font(None, 24)

# Função auxiliar para desenhar texto centralizado
def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    surf = fonte.render(texto, True, cor)
    texto_rect = surf.get_rect(center=rect.center)
    tela.blit(surf, texto_rect)


def abrir_nova_janela(tela_principal):
    """Abre janela para adicionar nova pergunta."""
    largura, altura = 800, 600
    nova_tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Adicionar Pergunta")

    margem = 20
    # Label da pergunta
    label_pergunta = FONTE_PADRAO.render("PERGUNTA", True, pygame.Color("white"))
    rect_label = label_pergunta.get_rect(topleft=(margem, margem))

    # Caixa de texto principal
    caixatexto = pygame.Rect(margem, rect_label.bottom + 10, 400, 100)
    texto_pergunta = ""
    ativo_pergunta = False

    # Alternativas
    rects_alt = [pygame.Rect(margem,
                     caixatexto.bottom + 20 + i * 50,
                     caixatexto.width, 40) for i in range(4)]
    textos_alt = [""] * 4
    ativos_alt = [False] * 4

    # Botões laterais (Adicionar / Cancelar)
    bw, bh, esp = 120, 40, 10
    x_lat = largura - margem - bw
    rect_add = pygame.Rect(x_lat, margem, bw, bh)
    rect_cancel = pygame.Rect(x_lat, margem + bh + esp, bw, bh)

    # Botão filtros
    rect_filt = pygame.Rect(margem, altura - margem - 30, 100, 30)
    filtros = ["fácil","médio","difícil","história","matemática","física","química","biologia","geometria","português","literatura"]
    sel_filtros = []
    mostrar = False
    rect_box = pygame.Rect(rect_filt.x, rect_filt.y - len(filtros)*30 - 10, 200, len(filtros)*30 + 10)
    rects_filt = [pygame.Rect(rect_box.x+5, rect_box.y+5 + i*30, rect_box.width-10,25) for i in range(len(filtros))]

    rodando = True
    retorno = "cancelar"

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "fechar_janela"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # Toggle filtros
                if mostrar and not rect_box.collidepoint(pos): mostrar = False
                if rect_filt.collidepoint(pos): mostrar = not mostrar
                # Caixa de texto pergunta
                if caixatexto.collidepoint(pos):
                    ativo_pergunta = True
                    ativos_alt = [False]*4
                else:
                    ativo_pergunta = False
                    for i,r in enumerate(rects_alt):
                        if r.collidepoint(pos):
                            ativos_alt = [False]*4; ativos_alt[i]=True; break
                # Botões laterais
                if rect_add.collidepoint(pos): print("Adicionar:", texto_pergunta, textos_alt, sel_filtros)
                elif rect_cancel.collidepoint(pos): rodando=False; retorno="cancelar"
                # Seleção de filtros
                if mostrar:
                    for i,r in enumerate(rects_filt):
                        if r.collidepoint(pos):
                            f=filtros[i]
                            sel_filtros.remove(f) if f in sel_filtros else sel_filtros.append(f)

            if evento.type == pygame.KEYDOWN:
                if ativo_pergunta:
                    if evento.key==pygame.K_BACKSPACE: texto_pergunta=texto_pergunta[:-1]
                    elif evento.key!=pygame.K_RETURN: texto_pergunta+=evento.unicode
                else:
                    for i, ativo in enumerate(ativos_alt):
                        if ativo:
                            if evento.key==pygame.K_BACKSPACE: textos_alt[i]=textos_alt[i][:-1]
                            elif evento.key!=pygame.K_RETURN: textos_alt[i]+=evento.unicode

        # Desenho
        nova_tela.fill(pygame.Color("black"))
        nova_tela.blit(label_pergunta, rect_label)

        # Pergunta
        cor_bg = pygame.Color("dimgray")
        cor_border = pygame.Color("dodgerblue") if ativo_pergunta else pygame.Color("gray")
        nova_tela.fill(cor_bg, caixatexto)
        pygame.draw.rect(nova_tela, cor_border, caixatexto,2,border_radius=5)
        surf = FONTE_PADRAO.render(texto_pergunta,True,pygame.Color("white"))
        nova_tela.blit(surf,(caixatexto.x+5,caixatexto.y+5))

        # Alternativas
        for i,r in enumerate(rects_alt):
            cor_b = pygame.Color("dodgerblue") if ativos_alt[i] else pygame.Color("gray")
            nova_tela.fill(cor_bg, r)
            pygame.draw.rect(nova_tela, cor_b,r,2,border_radius=5)
            rot=FONTE_PEQUENA.render(f"{chr(65+i)}.",True,pygame.Color("white"))
            nova_tela.blit(rot,(r.x-30, r.y+5))
            text=FONTE_PEQUENA.render(textos_alt[i],True,pygame.Color("white"))
            nova_tela.blit(text,(r.x+10,r.y+5))

        # Botões
        for rect, txt in [(rect_add,"ADICIONAR"),(rect_cancel,"CANCELAR"),(rect_filt,"FILTROS")]:
            cor_btn=pygame.Color("saddlebrown")
            nova_tela.fill(cor_btn, rect)
            desenhar_texto_centralizado(nova_tela, txt, FONTE_PEQUENA, pygame.Color("white"), rect)

        # Lista de filtros
        if mostrar:
            nova_tela.fill(cor_bg, rect_box)
            pygame.draw.rect(nova_tela,pygame.Color("gray"),rect_box,2,border_radius=5)
            for i,(f,r) in enumerate(zip(filtros,rects_filt)):
                bg=pygame.Color("green") if f in sel_filtros else pygame.Color("red")
                nova_tela.fill(bg,r)
                text=FONTE_PEQUENA.render(f,True,pygame.Color("white"))
                nova_tela.blit(text,(r.x+5,r.y+5))

        pygame.display.flip()

    return retorno

if __name__=='__main__':
    pygame.init()
    tela=pygame.display.set_mode((400,300))
    res=abrir_nova_janela(tela)
    print("Resultado:",res)
    pygame.quit()
