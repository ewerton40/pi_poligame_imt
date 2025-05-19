# Arquivo: Classes/addPerguntaTela.py
import pygame
from Classes.elementos_visuais import Cores, Fonte, desenhar_texto_centralizado
from Classes.componentes import criar_caixa_texto, desenhar_caixa_texto, criar_botao, desenhar_botao

def abrir_nova_janela(tela_principal):
    """Função para criar e exibir uma nova janela para adicionar perguntas."""
    largura_nova_janela = 800
    altura_nova_janela = 600
    nova_tela = pygame.display.set_mode((largura_nova_janela, altura_nova_janela))
    pygame.display.set_caption("Adicionar Pergunta")

    margem = 20
    texto_pergunta_label = Fonte.PADRAO.render("PERGUNTA", True, Cores.TEXTO)
    rect_pergunta_label = texto_pergunta_label.get_rect(topleft=(margem, margem))
    largura_caixa_texto = 400
    altura_caixa_texto = 100
    rect_caixa_texto = pygame.Rect(margem, rect_pergunta_label.bottom + 10, largura_caixa_texto, altura_caixa_texto)

    rect_alternativas = [pygame.Rect(margem, rect_caixa_texto.bottom + 20 + i * (40 + 10), largura_caixa_texto, 40) for i in range(4)]
    textos_alternativas = [""] * 4
    ativo_alternativas = [False] * 4

    texto_pergunta = ""
    ativo_pergunta = False

    largura_botao_lateral = 120
    altura_botao_lateral = 40
    espacamento_botao_lateral = 10
    x_botao_adicionar = largura_nova_janela - margem - largura_botao_lateral
    y_botao_adicionar = margem
    rect_botao_adicionar = pygame.Rect(x_botao_adicionar, y_botao_adicionar, largura_botao_lateral, altura_botao_lateral)
    y_botao_cancelar = y_botao_adicionar + altura_botao_lateral + espacamento_botao_lateral
    rect_botao_cancelar = pygame.Rect(x_botao_adicionar, y_botao_cancelar, largura_botao_lateral, altura_botao_lateral)

    largura_botao_inferior = 100
    altura_botao_inferior = 30
    x_botao_filtros = margem
    y_botao_inferior = altura_nova_janela - margem - altura_botao_inferior
    rect_botao_filtros = pygame.Rect(x_botao_filtros, y_botao_inferior, largura_botao_inferior, altura_botao_inferior)

    filtros_disponiveis = ["fácil", "médio", "difícil", "história", "matemática", "física", "química", "biologia", "geometria", "português", "literatura"]
    filtros_selecionados = []
    mostrar_filtros = False
    rect_filtros = pygame.Rect(rect_botao_filtros.x, rect_botao_filtros.y - len(filtros_disponiveis) * 30 - 10, 200, len(filtros_disponiveis) * 30 + 10)
    rects_filtros = [pygame.Rect(rect_filtros.x + 5, rect_filtros.y + 5 + i * 30, rect_filtros.width - 10, 25) for i in range(len(filtros_disponiveis))]

    rodando_nova_janela = True
    retorno = "cancelar"

    while rodando_nova_janela:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_nova_janela = False
                retorno = "fechar_janela"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()

                if mostrar_filtros and not rect_filtros.collidepoint(pos_mouse):
                    mostrar_filtros = False

                if rect_caixa_texto.collidepoint(pos_mouse):
                    ativo_pergunta = True
                    ativo_alternativas = [False] * 4
                else:
                    ativo_pergunta = False
                    for i in range(4):
                        if rect_alternativas[i].collidepoint(pos_mouse):
                            ativo_alternativas = [False] * 4
                            ativo_alternativas[i] = True
                            break

                if rect_botao_adicionar.collidepoint(pos_mouse):
                    print("Texto digitado:", texto_pergunta)
                    print("Alternativas:", textos_alternativas)
                    print("Filtros selecionados:", filtros_selecionados)
                elif rect_botao_cancelar.collidepoint(pos_mouse):
                    print("Botão CANCELAR clicado!")
                    retorno = "cancelar"
                    rodando_nova_janela = False
                elif rect_botao_filtros.collidepoint(pos_mouse):
                    mostrar_filtros = not mostrar_filtros

                if mostrar_filtros:
                    for i, rect_filtro in enumerate(rects_filtros):
                        if rect_filtro.collidepoint(pos_mouse):
                            filtro = filtros_disponiveis[i]
                            if filtro in filtros_selecionados:
                                filtros_selecionados.remove(filtro)
                            else:
                                filtros_selecionados.append(filtro)

            if evento.type == pygame.KEYDOWN:
                if ativo_pergunta:
                    if evento.key == pygame.K_RETURN:
                        ativo_pergunta = False
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_pergunta = texto_pergunta[:-1]
                    else:
                        texto_pergunta += evento.unicode
                else:
                    for i in range(4):
                        if ativo_alternativas[i]:
                            if evento.key == pygame.K_RETURN:
                                ativo_alternativas[i] = False
                            elif evento.key == pygame.K_BACKSPACE:
                                textos_alternativas[i] = textos_alternativas[i][:-1]
                            else:
                                textos_alternativas[i] += evento.unicode

        nova_tela.fill(Cores.FUNDO)
        nova_tela.blit(texto_pergunta_label, rect_pergunta_label)

        cor_borda_caixa_texto = Cores.BORDA_CAIXA_TEXTO_ATIVO if ativo_pergunta else Cores.BORDA_CAIXA_TEXTO_INATIVO
        pygame.draw.rect(nova_tela, Cores.CAIXA_TEXTO_FUNDO, rect_caixa_texto, 0, border_radius=5)
        pygame.draw.rect(nova_tela, cor_borda_caixa_texto, rect_caixa_texto, 2, border_radius=5)
        texto_renderizado_pergunta = Fonte.PADRAO.render(texto_pergunta, True, Cores.TEXTO)
        nova_tela.blit(texto_renderizado_pergunta, (rect_caixa_texto.x + 5, rect_caixa_texto.y + 5))

        for i in range(4):
            cor_borda = Cores.BORDA_CAIXA_TEXTO_ATIVO if ativo_alternativas[i] else Cores.BORDA_CAIXA_TEXTO_INATIVO
            pygame.draw.rect(nova_tela, Cores.CAIXA_TEXTO_FUNDO, rect_alternativas[i], 0, border_radius=5)
            pygame.draw.rect(nova_tela, cor_borda, rect_alternativas[i], 2, border_radius=5)
            rotulo = Fonte.PEQUENA.render(f"{chr(65+i)}.", True, Cores.TEXTO)
            nova_tela.blit(rotulo, (rect_alternativas[i].x - 30, rect_alternativas[i].y + 10))
            texto_alt = Fonte.PEQUENA.render(textos_alternativas[i], True, Cores.TEXTO)
            nova_tela.blit(texto_alt, (rect_alternativas[i].x + 10, rect_alternativas[i].y + 10))

        desenhar_botao(nova_tela, {"rect": rect_botao_adicionar, "texto": "ADICIONAR"})
        desenhar_botao(nova_tela, {"rect": rect_botao_cancelar, "texto": "CANCELAR"})
        desenhar_botao(nova_tela, {"rect": rect_botao_filtros, "texto": "FILTROS"})

        if mostrar_filtros:
            pygame.draw.rect(nova_tela, Cores.CAIXA_TEXTO_FUNDO, rect_filtros, 0, border_radius=5)
            pygame.draw.rect(nova_tela, Cores.BORDA_CAIXA_TEXTO_INATIVO, rect_filtros, 2, border_radius=5)
            for i, (filtro, rect_filtro) in enumerate(zip(filtros_disponiveis, rects_filtros)):
                cor_fundo = Cores.COR_FILTRO_SELECIONADO if filtro in filtros_selecionados else Cores.COR_FILTRO_NAO_SELECIONADO
                pygame.draw.rect(nova_tela, cor_fundo, rect_filtro, 0, border_radius=3)
                texto_filtro = Fonte.PEQUENA.render(filtro, True, Cores.TEXTO)
                nova_tela.blit(texto_filtro, (rect_filtro.x + 5, rect_filtro.y + 5))

        pygame.display.flip()

    return retorno

if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Teste Adicionar Pergunta")
    resultado = abrir_nova_janela(tela_teste)
    print(f"Ação da janela de adicionar pergunta: {resultado}")
    pygame.quit()