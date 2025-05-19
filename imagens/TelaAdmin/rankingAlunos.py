import pygame

# Inicialização do Pygame e da fonte
pygame.init()
pygame.font.init()

# Definições de cores
COR_DE_FUNDO = (220, 220, 220)  # Cinza claro
COR_TEXTO = (0, 0, 0)  # Preto
COR_CABECALHO = (80, 80, 80)  # Cinza escuro
COR_TEXTO_CABECALHO = (255, 255, 255)  # Branco
COR_LINHA = (50, 50, 50)  # Cinza mais escuro
COR_BOTAO_FECHAR = (80, 80, 80)
COR_TEXTO_FECHAR = (255, 255, 255)

# Fonte padrão
fonte = pygame.font.Font(None, 24)  # Diminuindo a fonte padrão
fonte_cabecalho = pygame.font.Font(None, 22)  # Diminuindo a fonte do cabeçalho
fonte_fechar = pygame.font.Font(None, 20)  # Diminuindo a fonte do botão fechar

# Dados de exemplo para o ranking (lista de dicionários)
ranking_data = [
    {"nome": "João", "pontuacao": "$25071", "identificacao": "25.00873-1", "turma": "t3sub2"},
    {"nome": "Maria", "pontuacao": "$23456", "identificacao": "25.00123-4", "turma": "t1sub1"},
    {"nome": "Carlos", "pontuacao": "$21890", "identificacao": "25.00987-6", "turma": "t2sub3"},
    {"nome": "Ana", "pontuacao": "$20123", "identificacao": "25.00543-2", "turma": "t3sub1"},
    {"nome": "Pedro", "pontuacao": "$18765", "identificacao": "25.00234-5", "turma": "t1sub2"},
    {"nome": "Sofia", "pontuacao": "$17432", "identificacao": "25.00678-9", "turma": "t2sub2"},
    {"nome": "Lucas", "pontuacao": "$16098", "identificacao": "25.00345-8", "turma": "t3sub3"},
    {"nome": "Isabela", "pontuacao": "$15789", "identificacao": "25.00789-0", "turma": "t1sub3"},
    {"nome": "Gabriel", "pontuacao": "$14567", "identificacao": "25.00456-3", "turma": "t2sub1"},
    {"nome": "Manuela", "pontuacao": "$13234", "identificacao": "25.00890-1", "turma": "t3sub2"},
    # Adicione mais dados aqui
]

def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    """Desenha um texto centralizado dentro de um retângulo."""
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    tela.blit(texto_renderizado, texto_rect)

def abrir_janela2(tela_principal):
    """Cria e exibe a janela de ranking adaptada para 800x600."""
    largura_da_tela = 800
    altura_da_tela = 600
    tela_ranking = pygame.Surface((largura_da_tela, altura_da_tela))
    rect_tela_ranking = tela_ranking.get_rect(center=tela_principal.get_rect().center)

    margem = 10  # Diminuindo a margem
    altura_cabecalho = 40  # Diminuindo a altura do cabeçalho
    espacamento_cabecalho = 5  # Diminuindo o espaçamento do cabeçalho
    largura_coluna = (largura_da_tela - 2 * margem - 3 * espacamento_cabecalho) // 4
    altura_linha = 30  # Diminuindo a altura da linha
    espacamento_linha = 5  # Diminuindo o espaçamento da linha
    margem_topo_lista = margem + altura_cabecalho + 2 * espacamento_cabecalho

    # Retângulos dos cabeçalhos
    rect_nome = pygame.Rect(margem, margem, largura_coluna, altura_cabecalho)
    rect_pontuacao = pygame.Rect(margem + largura_coluna + espacamento_cabecalho, margem, largura_coluna, altura_cabecalho)
    rect_identificacao = pygame.Rect(margem + 2 * (largura_coluna + espacamento_cabecalho), margem, largura_coluna, altura_cabecalho)
    rect_turma = pygame.Rect(margem + 3 * (largura_coluna + espacamento_cabecalho), margem, largura_coluna, altura_cabecalho)

    # Botão "FECHAR"
    largura_botao_fechar = 80  # Diminuindo a largura do botão
    altura_botao_fechar = 25  # Diminuindo a altura do botão
    rect_botao_fechar = pygame.Rect(largura_da_tela - margem - largura_botao_fechar, altura_da_tela - margem - altura_botao_fechar, largura_botao_fechar, altura_botao_fechar)

    rodando_ranking = True
    while rodando_ranking:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_ranking = False
                return False  # Indica que o jogo principal deve fechar
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                # Ajusta a posição do mouse para a superfície da tela de ranking
                pos_mouse_ranking = (pos_mouse[0] - rect_tela_ranking.left, pos_mouse[1] - rect_tela_ranking.top)
                if rect_botao_fechar.collidepoint(pos_mouse_ranking):
                    rodando_ranking = False
                    return True  # Indica que deve voltar para a tela principal

        # Desenha a tela de ranking na superfície
        tela_ranking.fill(COR_DE_FUNDO)

        # Desenha os cabeçalhos
        pygame.draw.rect(tela_ranking, COR_CABECALHO, rect_nome, border_radius=3)  # Diminuindo o border_radius
        desenhar_texto_centralizado(tela_ranking, "NOME", fonte_cabecalho, COR_TEXTO_CABECALHO, rect_nome)

        pygame.draw.rect(tela_ranking, COR_CABECALHO, rect_pontuacao, border_radius=3)  # Diminuindo o border_radius
        desenhar_texto_centralizado(tela_ranking, "PONTUAÇÃO", fonte_cabecalho, COR_TEXTO_CABECALHO, rect_pontuacao)

        pygame.draw.rect(tela_ranking, COR_CABECALHO, rect_identificacao, border_radius=3)  # Diminuindo o border_radius
        desenhar_texto_centralizado(tela_ranking, "IDENTIFICAÇÃO", fonte_cabecalho, COR_TEXTO_CABECALHO, rect_identificacao)

        pygame.draw.rect(tela_ranking, COR_CABECALHO, rect_turma, border_radius=3)  # Diminuindo o border_radius
        desenhar_texto_centralizado(tela_ranking, "TURMA", fonte_cabecalho, COR_TEXTO_CABECALHO, rect_turma)

        # Desenha o botão "FECHAR"
        pygame.draw.rect(tela_ranking, COR_BOTAO_FECHAR, rect_botao_fechar, border_radius=3)  # Diminuindo o border_radius
        desenhar_texto_centralizado(tela_ranking, "FECHAR", fonte_fechar, COR_TEXTO_FECHAR, rect_botao_fechar)

        # Desenha as linhas e os dados do ranking
        y_linha = margem_topo_lista
        for data in ranking_data:
            pygame.draw.rect(tela_ranking, COR_LINHA, (margem, y_linha, largura_da_tela - 2 * margem, altura_linha), border_radius=2)  # Diminuindo o border_radius

            # Desenha os dados em cada coluna
            texto_nome = fonte.render(data["nome"], True, COR_TEXTO)
            tela_ranking.blit(texto_nome, (margem + 5, y_linha + altura_linha // 2 - texto_nome.get_height() // 2))  # Diminuindo a margem interna

            texto_pontuacao = fonte.render(data["pontuacao"], True, COR_TEXTO)
            tela_ranking.blit(texto_pontuacao, (rect_pontuacao.left + 5, y_linha + altura_linha // 2 - texto_pontuacao.get_height() // 2))  # Diminuindo a margem interna

            texto_identificacao = fonte.render(data["identificacao"], True, COR_TEXTO)
            tela_ranking.blit(texto_identificacao, (rect_identificacao.left + 5, y_linha + altura_linha // 2 - texto_identificacao.get_height() // 2))  # Diminuindo a margem interna

            texto_turma = fonte.render(data["turma"], True, COR_TEXTO)
            tela_ranking.blit(texto_turma, (rect_turma.left + 5, y_linha + altura_linha // 2 - texto_turma.get_height() // 2))  # Diminuindo a margem interna

            y_linha += altura_linha + espacamento_linha

        tela_principal.blit(tela_ranking, rect_tela_ranking)
        pygame.display.flip()
        

    return True # Indica que deve voltar para a tela principal