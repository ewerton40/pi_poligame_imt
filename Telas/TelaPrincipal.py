import pygame
import sys

pygame.init()
resolucao_original_x = 1920
resolucao_original_y = 1080
resolucao_desejada_x = 1280
resolucao_desejada_y = 720

screen = pygame.display.set_mode((resolucao_desejada_x, resolucao_desejada_y))
pygame.display.set_caption("Quiz com Fundo Imagem")

# Função para escalar coordenadas e tamanhos
def escalar(valor):
    return int(valor * (resolucao_desejada_x / resolucao_original_x))

# Função para escalar coordenadas Y
def escalar_y(valor):
    return int(valor * (resolucao_desejada_y / resolucao_original_y))

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Cor azul para o texto de acerto
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER = (80, 80, 80)
SELECTED_COLOR = (100, 150, 200)  # Cor para alternativa selecionada

font_question = pygame.font.SysFont('Arial', escalar(48))
font_alternative = pygame.font.SysFont('Arial', escalar(36))
font_button = pygame.font.SysFont('Arial', escalar(40))
font_acerto = pygame.font.SysFont('Arial', escalar(120), bold=True) # Fonte maior e em negrito para o acerto

background_original = pygame.image.load("imagens/Prancheta 2.png")
background = pygame.transform.scale(background_original, (resolucao_desejada_x, resolucao_desejada_y))

botao_premio_rect = pygame.Rect(escalar(1500), escalar_y(0), escalar(250), escalar_y(80))
area_premio = pygame.Rect(escalar(500), escalar_y(700), escalar(200), escalar_y(60))
area_pergunta = pygame.Rect(escalar(80), escalar_y(70), escalar(1400), escalar_y(150))

# Dicionário de alternativas
alternativas_dict = {
    "A": "Rio de Janeiro",
    "B": "São Paulo",
    "C": "Brasília",
    "D": "Minas gerais"
}

# Define as áreas para as alternativas baseadas no dicionário
areas_alternativas = {}
y_offset_inicial = escalar_y(380)
altura_alternativa = escalar_y(100)
espacamento_vertical = escalar_y(70)  # Espaçamento entre as caixas

for chave, texto in alternativas_dict.items():
    posicao_y = y_offset_inicial + (list(alternativas_dict.keys()).index(chave)) * (altura_alternativa + espacamento_vertical)
    areas_alternativas[chave] = pygame.Rect(escalar(50), posicao_y, escalar(900), altura_alternativa)

btn_confirmar = pygame.Rect(escalar(200), escalar_y(1010), escalar(200), escalar_y(60))
btn_parar = pygame.Rect(escalar(550), escalar_y(1010), escalar(200), escalar_y(60))
#TEXTO PERGUNTAS
pergunta = "Qual a capital do brasil?."

# Variável para armazenar a alternativa selecionada (agora a chave do dicionário)
alternativa_selecionada = None
# Variável de estado para controlar a exibição da mensagem de acerto
mostrar_acerto = False

def desenhar_texto_quebrado(surface, texto, font, color, rect):
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
    espacamento_linhas = escalar_y(10)  # Espaçamento entre as linhas
    for linha in linhas:
        texto_renderizado = font.render(linha.strip(), True, color)
        texto_rect = texto_renderizado.get_rect(topleft=(rect.left, y_offset))
        surface.blit(texto_renderizado, texto_rect)
        y_offset += texto_renderizado.get_height() + espacamento_linhas

def desenhar_botao(rect, texto, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR

    # Desenha a borda preta
    pygame.draw.rect(screen, BLACK, rect)

    # Reduz o retângulo em 4px de cada lado para a parte interna (o botão)
    inner_rect = rect.inflate(-escalar(16), -escalar_y(16))
    pygame.draw.rect(screen, color, inner_rect)

    # Desenha o texto centralizado no botão interno
    text_surf = font_button.render(texto, True, WHITE)
    text_rect = text_surf.get_rect(center=inner_rect.center)
    screen.blit(text_surf, text_rect)

def desenhar_alternativa(surface, rect, texto, selecionada=False, hover=False):
    # Cor de fundo da alternativa
    if selecionada:
        color = SELECTED_COLOR
    elif hover:
        color = BUTTON_HOVER
    else:
        color = WHITE

    # Desenha a borda preta
    pygame.draw.rect(surface, BLACK, rect)

    # Desenha o fundo interno
    inner_rect = rect.inflate(-escalar(16), -escalar_y(16))
    pygame.draw.rect(surface, color, inner_rect)

    # Desenha o texto
    text_surf = font_alternative.render(f"{texto}", True, BLACK)
    text_rect = text_surf.get_rect(midleft=(inner_rect.x + escalar(10), inner_rect.centery))
    surface.blit(text_surf, text_rect)

def desenhar_botao_premio(surface, rect, texto, fonte, cor_texto, cor_fundo, cor_borda):
    # Desenha a borda
    pygame.draw.rect(surface, cor_borda, rect)

    # Reduz o retângulo para a parte interna do botão
    inner_rect = rect.inflate(-escalar(16), -escalar_y(16))

    # Desenha o fundo do botão
    pygame.draw.rect(surface, cor_fundo, inner_rect)

    # Renderiza o texto
    texto_surf = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surf.get_rect(center=inner_rect.center)

    # Blita o texto no centro do botão
    surface.blit(texto_surf, texto_rect)

running = True
while running:
    screen.blit(background, (0, 0))

    desenhar_texto_quebrado(screen, pergunta, font_question, WHITE, area_pergunta)

    mouse_pos = pygame.mouse.get_pos()

    # Verifica hover nas alternativas
    hover_alternativas = {}
    for chave, area in areas_alternativas.items():
        hover_alternativas[chave] = area.collidepoint(mouse_pos)

    # Desenha as alternativas usando o dicionário
    for chave, texto in alternativas_dict.items():
        area = areas_alternativas[chave]
        selecionada = (chave == alternativa_selecionada)
        hover = hover_alternativas[chave]
        desenhar_alternativa(screen, area, f"{chave}) {texto}", selecionada, hover)

    # Verifica hover nos botões
    hover_confirmar = btn_confirmar.collidepoint(mouse_pos)
    hover_parar = btn_parar.collidepoint(mouse_pos)

    desenhar_botao(btn_confirmar, "Confirmar", hover_confirmar)
    desenhar_botao(btn_parar, "Parar", hover_parar)

    # Se a variável mostrar_acerto for True, desenha a mensagem
    if mostrar_acerto:
        texto_acerto = font_acerto.render("ACERTOU!!!", True, BLUE)
        texto_acerto_rect = texto_acerto.get_rect(center=screen.get_rect().center)
        screen.blit(texto_acerto, texto_acerto_rect)

    desenhar_botao_premio(screen, botao_premio_rect, "PRÊMIO", font_button, WHITE, RED, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifica clique nas alternativas (agora usando o dicionário)
            for chave, area in areas_alternativas.items():
                if area.collidepoint(event.pos):
                    alternativa_selecionada = chave
                    print(f"Alternativa selecionada: {chave} - {alternativas_dict[chave]}")
                    break

            if btn_confirmar.collidepoint(event.pos):
                print("Botão Confirmar clicado!")
                if alternativa_selecionada is not None:
                    print(f"Confirmando alternativa: {alternativa_selecionada} - {alternativas_dict[alternativa_selecionada]}")
                    # *** AQUI VOCÊ DEVE COLOCAR A LÓGICA PARA VERIFICAR SE A RESPOSTA ESTÁ CORRETA ***
                    # Para este exemplo, vamos considerar que qualquer seleção é um acerto.
                    mostrar_acerto = True
                else:
                    print("Nenhuma alternativa selecionada!")

            elif btn_parar.collidepoint(event.pos):
                print("Botão Parar clicado!")
                running = False

            if botao_premio_rect.collidepoint(event.pos):
                print("Botão PRÊMIO clicado!")
                # Aqui você pode adicionar a ação que acontece ao clicar no botão

    pygame.display.flip()

pygame.quit()
sys.exit()