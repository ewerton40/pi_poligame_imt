import pygame
from addPerguntaTela import abrir_nova_janela
from rankingAlunos import abrir_janela2
from adicionarAluno import abrir_tela_adicionar_aluno

# Inicialização do Pygame
pygame.init()

# Definições de cores
COR_DE_FUNDO = (220, 220, 220)
COR_BOTOES_MENU = (80, 80, 80)
COR_TEXTO_BOTOES = (255, 255, 255)
COR_LISTA_ITEM = (50, 50, 50)
COR_TEXTO_LISTA = (255, 255, 255)
COR_BOTAO_FILTRO = (128, 128, 128)
COR_BOTAO_EDITAR = (160, 82, 45)

# Dimensões da tela
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tela de Gerenciamento")

# Fonte padrão
fonte = pygame.font.Font(None, 30)
fonte_pequena = pygame.font.Font(None, 24)

# Funções para desenhar
def desenhar_botao(texto, x, y, largura, altura, cor, cor_texto, funcao=None):
    pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius=5)
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_renderizado, texto_rect)
    return pygame.Rect(x, y, largura, altura)

def desenhar_item_lista(texto_pergunta, y, largura_total):
    altura_item = 50
    margem = 10
    x_item = margem
    largura_item = largura_total - 2 * margem
    pygame.draw.rect(tela, COR_LISTA_ITEM, (x_item, y, largura_item, altura_item), border_radius=5)
    texto_renderizado = fonte.render(texto_pergunta, True, COR_TEXTO_LISTA)
    texto_rect = texto_renderizado.get_rect(midleft=(x_item + margem, y + altura_item // 2))
    tela.blit(texto_renderizado, texto_rect)
    largura_botao_filtro = 80
    altura_botao_filtro = 30
    espacamento_filtro = 30
    x_filtro1 = x_item + largura_item - 3 * largura_botao_filtro - 2 * espacamento_filtro - margem
    x_filtro2 = x_item + largura_item - 2 * largura_botao_filtro - espacamento_filtro - margem
    x_filtro3 = x_item + largura_item - largura_botao_filtro - margem
    y_botao = y + (altura_item - altura_botao_filtro) // 2
    botao_filtro1_rect = desenhar_botao("Filtro()", x_filtro1, y_botao, largura_botao_filtro, altura_botao_filtro, COR_BOTAO_FILTRO, COR_TEXTO_BOTOES, "filtrar")
    botao_filtro2_rect = desenhar_botao("Filtro()", x_filtro2, y_botao, largura_botao_filtro, altura_botao_filtro, COR_BOTAO_FILTRO, COR_TEXTO_BOTOES, "filtrar")
    botao_filtro3_rect = desenhar_botao("Filtro()", x_filtro3, y_botao, largura_botao_filtro, altura_botao_filtro, COR_BOTAO_FILTRO, COR_TEXTO_BOTOES, "filtrar")
    largura_botao_editar = 80
    botao_editar_rect = desenhar_botao("EDITAR", x_item + largura_item - largura_botao_editar - margem, y_botao, largura_botao_editar, altura_botao_filtro, COR_BOTAO_EDITAR, COR_TEXTO_BOTOES, "editar")
    return [botao_filtro1_rect, botao_filtro2_rect, botao_filtro3_rect, botao_editar_rect]

# Posições e dimensões dos elementos
margem_superior = 20
altura_menu = 60
largura_botao_menu = 140
espacamento_menu = 10

# Botões do menu superior
# Posições e dimensões dos elementos
margem_superior = 20
altura_menu = 60
largura_botao_menu = 140
num_botoes_menu = 5  # Número de botões no menu

# Calcular o espaço total ocupado pelos botões
largura_total_botoes = num_botoes_menu * largura_botao_menu

# Calcular o espaço disponível para os espaçamentos (considerando uma margem inicial e final)
espaco_disponivel = LARGURA_TELA - largura_total_botoes

# Calcular o número de espaços entre os botões
num_espacos = num_botoes_menu + 1 # Incluindo espaço antes do primeiro e depois do último

# Calcular o espaçamento uniforme
espacamento_uniforme = espaco_disponivel // num_espacos

# Botões do menu superior (alinhados à direita)
botoes_menu_data = []
x_atual = LARGURA_TELA - espacamento_uniforme - largura_botao_menu
for i, texto_botao in enumerate(reversed(["Criar", "Procurar", "Filtrar", "Add Aluno", "Ranking"])):
    botao_data = {
        "texto": texto_botao,
        "x": x_atual,
        "y": margem_superior,
        "largura": largura_botao_menu,
        "altura": altura_menu,
        "funcao": texto_botao.lower().replace(" ", "_")
    }
    botoes_menu_data.append(botao_data)
    x_atual -= largura_botao_menu + espacamento_uniforme

botoes_menu_rects = []
for data in reversed(botoes_menu_data): # Reverter novamente para a ordem original ao desenhar
    rect = pygame.Rect(data["x"], data["y"], data["largura"], data["altura"])
    botoes_menu_rects.append((rect, data["texto"], data["funcao"]))

# Label "Mostrar" e lista de perguntas
texto_mostrar = fonte.render("Perguntas", True, (0, 0, 0))
rect_mostrar = texto_mostrar.get_rect(topleft=(espacamento_menu, margem_superior + altura_menu + 20))
perguntas = ["Pergunta 1"]
altura_item_lista = 50
espacamento_lista = 10
y_inicial_lista = rect_mostrar.bottom + 20
itens_lista_rects = []

def criar_novo_elemento():
    """Esta função será executada quando o botão 'Criar' for clicado e abrirá a nova janela."""
    print("Botão 'Criar' foi clicado! Abrindo nova janela.")
    retorno_janela_criar = abrir_nova_janela(tela) # Passa a tela principal e espera o retorno
    if retorno_janela_criar == "cancelar":
        print("Criação de pergunta cancelada.")
    elif retorno_janela_criar == "adicionar":
        print("Pergunta adicionada (lógica de adicionar aqui).")
        # Aqui você implementaria a lógica para realmente adicionar a pergunta
        # à sua lista 'perguntas' ou a outra estrutura de dados.
    elif retorno_janela_criar == "fechar_janela":
        print("Janela de adicionar pergunta fechada.")

def ranking_alunos_chamado():
    """Esta função será executada quando o botão 'ranking' for clicado e abrirá a tela de ranking."""
    print("Botão 'ranking' foi clicado! Abrindo tela de ranking.")
    retorno_ranking = abrir_janela2(tela)
    if not retorno_ranking:
        global rodando
        rodando = False

def adicionar_aluno_chamado():
    """Função para abrir a tela de adicionar aluno."""
    print("Botão 'Add Aluno' clicado! Abrindo tela de adicionar aluno.")
    retorno_adicionar_aluno = abrir_tela_adicionar_aluno(tela)
    if retorno_adicionar_aluno == "cancelar":
        print("Adição de aluno cancelada.")
    elif retorno_adicionar_aluno == "adicionar_aluno":
        print("Dados do aluno a serem processados.")
        # Aqui você implementaria a lógica para adicionar o aluno
    elif retorno_adicionar_aluno == "fechar_janela":
        print("Janela de adicionar aluno fechada.")

# Loop principal do jogo
rodando = True
while rodando:
    tela.fill(COR_DE_FUNDO)

    # Desenha os botões do menu superior
    for rect, texto, funcao in botoes_menu_rects:
        desenhar_botao(texto, rect.x, rect.y, rect.width, rect.height, COR_BOTOES_MENU, COR_TEXTO_BOTOES)

    # Desenha o label "Mostrar"
    tela.blit(texto_mostrar, rect_mostrar)

    # Desenha a lista de perguntas
    itens_lista_rects = []
    for i, pergunta in enumerate(perguntas):
        y_item = y_inicial_lista + i * (altura_item_lista + espacamento_lista)
        rects_item = desenhar_item_lista(pergunta, y_item, LARGURA_TELA)
        itens_lista_rects.append(rects_item)

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()
            # Verificar cliques nos botões do menu
            for rect, texto, funcao in botoes_menu_rects:
                if rect.collidepoint(pos_mouse):
                    print(f"Botão '{texto}' clicado. Função: {funcao}")
                    if texto == "Criar":
                        criar_novo_elemento()
                    elif texto == "Ranking":
                        ranking_alunos_chamado()
                    # Adicione aqui a lógica para outros botões do menu, se necessário
                    elif texto == "Add Aluno":
                        adicionar_aluno_chamado()

            # Verificar cliques nos botões dos itens da lista (apenas para demonstração)
            for lista_item_rects in itens_lista_rects:
                for rect in lista_item_rects:
                    if rect.collidepoint(pos_mouse):
                        print(f"Botão da lista clicado: {rect}")

pygame.quit()