import pygame

# Inicialize o módulo de fonte do Pygame
pygame.font.init()

# Definições de cores
COR_DE_FUNDO = (220, 220, 220)
COR_TEXTO = (0, 0, 0)
COR_CAIXA_TEXTO_FUNDO = (255, 255, 255)  # Alterado para branco para melhor visualização do texto
COR_BOTAO = (80, 80, 80)
COR_TEXTO_BOTAO = (255, 255, 255)
COR_BORDA_CAIXA_TEXTO_ATIVO = (0, 128, 255)  # Azul claro para indicar que está ativo
COR_BORDA_CAIXA_TEXTO_INATIVO = (100, 100, 100) # Cinza para quando não está ativo

# Fonte padrão
fonte = pygame.font.Font(None, 30)
fonte_pequena = pygame.font.Font(None, 24)

def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    tela.blit(texto_renderizado, texto_rect)

def abrir_nova_janela(tela_principal): # Recebe a tela principal como argumento
    """Função para criar e exibir uma nova janela para adicionar perguntas."""
    largura_nova_janela = 800
    altura_nova_janela = 600
    nova_tela = pygame.display.set_mode((largura_nova_janela, altura_nova_janela))
    pygame.display.set_caption("Adicionar Pergunta")

    # Posições e dimensões dos elementos
    margem = 20
    texto_pergunta_label = fonte.render("PERGUNTA", True, COR_TEXTO)
    rect_pergunta_label = texto_pergunta_label.get_rect(topleft=(margem, margem))
    largura_caixa_texto = 400
    altura_caixa_texto = 100
    rect_caixa_texto = pygame.Rect(margem, rect_pergunta_label.bottom + 10, largura_caixa_texto, altura_caixa_texto)

    # Variáveis para a caixa de texto
    texto_pergunta = ""
    ativo_pergunta = False # Indica se a caixa de texto está ativa para receber entrada

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
    espacamento_botao_inferior = 10
    x_botao_filtros = margem
    y_botao_inferior = altura_nova_janela - margem - altura_botao_inferior
    rect_botao_filtros = pygame.Rect(x_botao_filtros, y_botao_inferior, largura_botao_inferior, altura_botao_inferior)
    x_botao_dicas = x_botao_filtros + largura_botao_inferior + espacamento_botao_inferior
    rect_botao_dicas = pygame.Rect(x_botao_dicas, y_botao_inferior, largura_botao_inferior, altura_botao_inferior)
    x_botao_materia = x_botao_dicas + largura_botao_inferior + largura_botao_inferior
    rect_botao_materia = pygame.Rect(x_botao_materia, y_botao_inferior, largura_botao_inferior, altura_botao_inferior)

    rodando_nova_janela = True
    retorno = "cancelar" # Valor padrão de retorno

    while rodando_nova_janela:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_nova_janela = False
                retorno = "fechar_janela"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                # Ativa/desativa a caixa de texto ao clicar nela
                if rect_caixa_texto.collidepoint(pos_mouse):
                    ativo_pergunta = True
                else:
                    ativo_pergunta = False

                if rect_botao_adicionar.collidepoint(pos_mouse):
                    print("Texto digitado:", texto_pergunta) # Imprime no terminal
                    # Você pode manter ou remover a linha abaixo, dependendo se quer fechar a janela ao adicionar
                    # retorno = "adicionar"
                    # rodando_nova_janela = False
                elif rect_botao_cancelar.collidepoint(pos_mouse):
                    print("Botão CANCELAR clicado!")
                    retorno = "cancelar"
                    rodando_nova_janela = False
                elif rect_botao_filtros.collidepoint(pos_mouse):
                    print("Botão FILTROS clicado!")
                elif rect_botao_dicas.collidepoint(pos_mouse):
                    print("Botão DICAS clicado!")
                elif rect_botao_materia.collidepoint(pos_mouse):
                    print("Botão MATERIA clicado!")

            if evento.type == pygame.KEYDOWN:
                if ativo_pergunta:
                    if evento.key == pygame.K_RETURN:
                        ativo_pergunta = False # Desativa ao pressionar Enter (opcional)
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_pergunta = texto_pergunta[:-1] # Apaga o último caractere
                    else:
                        texto_pergunta += evento.unicode # Adiciona o caractere digitado

        # Desenha os elementos na tela
        nova_tela.fill(COR_DE_FUNDO)
        nova_tela.blit(texto_pergunta_label, rect_pergunta_label)

        # Desenha a caixa de texto
        cor_borda_caixa_texto = COR_BORDA_CAIXA_TEXTO_ATIVO if ativo_pergunta else COR_BORDA_CAIXA_TEXTO_INATIVO
        pygame.draw.rect(nova_tela, COR_CAIXA_TEXTO_FUNDO, rect_caixa_texto, 0, border_radius=5) # Preenche o fundo
        pygame.draw.rect(nova_tela, cor_borda_caixa_texto, rect_caixa_texto, 2, border_radius=5) # Desenha a borda

        # Renderiza e blita o texto dentro da caixa
        texto_renderizado_pergunta = fonte.render(texto_pergunta, True, COR_TEXTO)
        nova_tela.blit(texto_renderizado_pergunta, (rect_caixa_texto.x + 5, rect_caixa_texto.y + 5))

        pygame.draw.rect(nova_tela, COR_BOTAO, rect_botao_adicionar, border_radius=5)
        desenhar_texto_centralizado(nova_tela, "ADICIONAR", fonte_pequena, COR_TEXTO_BOTAO, rect_botao_adicionar)
        pygame.draw.rect(nova_tela, COR_BOTAO, rect_botao_cancelar, border_radius=5)
        desenhar_texto_centralizado(nova_tela, "CANCELAR", fonte_pequena, COR_TEXTO_BOTAO, rect_botao_cancelar)
        pygame.draw.rect(nova_tela, COR_BOTAO, rect_botao_filtros, border_radius=5)
        desenhar_texto_centralizado(nova_tela, "FILTROS", fonte_pequena, COR_TEXTO_BOTAO, rect_botao_filtros)
        pygame.draw.rect(nova_tela, COR_BOTAO, rect_botao_dicas, border_radius=5)
        desenhar_texto_centralizado(nova_tela, "DICAS", fonte_pequena, COR_TEXTO_BOTAO, rect_botao_dicas)
        pygame.draw.rect(nova_tela, COR_BOTAO, rect_botao_materia, border_radius=5)
        desenhar_texto_centralizado(nova_tela, "MATERIA", fonte_pequena, COR_TEXTO_BOTAO, rect_botao_materia)

        pygame.display.flip()

    pygame.display.flip() # Fecha apenas a janela de adicionar pergunta
    return retorno

if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Teste Adicionar Pergunta")
    resultado = abrir_nova_janela(tela_teste)
    print(f"Ação da janela de adicionar pergunta: {resultado}")
    pygame.display.flip()