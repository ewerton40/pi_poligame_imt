import pygame

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Definições de cores
COR_DE_FUNDO = (220, 220, 220)  # Cinza claro
COR_TEXTO = (255, 255, 255)  # Branco
COR_CAIXA_TEXTO_FUNDO = (50, 50, 50)  # Cinza escuro
COR_BOTAO = (80, 80, 80)  # Cinza escuro (botões)
COR_TEXTO_BOTAO = (255, 255, 255)  # Branco (texto dos botões)
COR_BORDA_CAIXA_TEXTO_ATIVO = (0, 128, 255)  # Azul claro (borda da caixa de texto ativa)
COR_BORDA_CAIXA_TEXTO_INATIVO = (100, 100, 100)  # Cinza médio (borda da caixa de texto inativa)

# Fonte padrão
fonte = pygame.font.Font(None, 30)
fonte_pequena = pygame.font.Font(None, 24)

def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    texto_renderizado = fonte.render(texto, True, cor)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    tela.blit(texto_renderizado, texto_rect)

def criar_caixa_texto(x, y, largura, altura, texto_inicial="", texto_label=""):
    rect = pygame.Rect(x, y, largura, altura)
    texto = texto_inicial
    label = texto_label
    ativo = False
    return {"rect": rect, "texto": texto, "label": label, "ativo": ativo}

def desenhar_caixa_texto(tela, caixa):
    cor_borda = COR_BORDA_CAIXA_TEXTO_ATIVO if caixa["ativo"] else COR_BORDA_CAIXA_TEXTO_INATIVO
    pygame.draw.rect(tela, COR_CAIXA_TEXTO_FUNDO, caixa["rect"], 0, border_radius=10)
    pygame.draw.rect(tela, cor_borda, caixa["rect"], 2, border_radius=10)
    texto_renderizado = fonte.render(caixa["texto"], True, COR_TEXTO)
    tela.blit(texto_renderizado, (caixa["rect"].x + 10, caixa["rect"].y + (caixa["rect"].height - texto_renderizado.get_height()) // 2))
    texto_label_renderizado = fonte_pequena.render(caixa["label"], True, COR_TEXTO)
    tela.blit(texto_label_renderizado, (caixa["rect"].x + 10, caixa["rect"].y - texto_label_renderizado.get_height() - 5))

def criar_botao(texto, x, y, largura, altura):
    rect = pygame.Rect(x, y, largura, altura)
    return {"rect": rect, "texto": texto}

def desenhar_botao(tela, botao):
    pygame.draw.rect(tela, COR_BOTAO, botao["rect"], 0, border_radius=10)
    desenhar_texto_centralizado(tela, botao["texto"], fonte_pequena, COR_TEXTO_BOTAO, botao["rect"])
    return botao["rect"]

def abrir_tela_adicionar_aluno(tela_principal):
    """Função para criar e exibir a tela de adicionar aluno."""
    largura_tela = 800
    altura_tela = 600
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Adicionar Aluno")

    caixa_email = criar_caixa_texto(20, 50, 250, 40, texto_label="EMAIL")
    caixa_senha = criar_caixa_texto(20, 120, 250, 40, texto_label="SENHA")

    botao_adicionar = criar_botao("ADICIONAR", 290, 45, 100, 40)
    botao_cancelar = criar_botao("CANCELAR", 290, 115, 100, 40)

    caixas_texto = [caixa_email, caixa_senha]
    botoes = [botao_adicionar, botao_cancelar]

    rodando = True
    retorno = "cancelar"

    while rodando:
        tela.fill(COR_DE_FUNDO)

        for caixa in caixas_texto:
            desenhar_caixa_texto(tela, caixa)

        for botao in botoes:
            desenhar_botao(tela, botao)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "fechar_janela"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                for i, caixa in enumerate(caixas_texto):
                    if caixa["rect"].collidepoint(pos_mouse):
                        caixa["ativo"] = True
                    else:
                        caixa["ativo"] = False

                if botao_adicionar["rect"].collidepoint(pos_mouse):
                    email = caixa_email["texto"]
                    senha = caixa_senha["texto"]
                    print(f"Adicionar Aluno - Email: {email}, Senha: {senha}")
                    retorno = "adicionar_aluno" # Sinaliza que o botão adicionar foi clicado
                    rodando = False
                elif botao_cancelar["rect"].collidepoint(pos_mouse):
                    print("Adicionar Aluno - Cancelado")
                    retorno = "cancelar"
                    rodando = False
            if evento.type == pygame.KEYDOWN:
                for caixa in caixas_texto:
                    if caixa["ativo"]:
                        if evento.key == pygame.K_RETURN:
                            caixa["ativo"] = False
                        elif evento.key == pygame.K_BACKSPACE:
                            caixa["texto"] = caixa["texto"][:-1]
                        else:
                            caixa["texto"] += evento.unicode

    pygame.display.flip()
    return retorno
    return retorno

if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Teste Adicionar Aluno")
    resultado = abrir_tela_adicionar_aluno(tela_teste)
    print(f"Resultado da tela de adicionar aluno: {resultado}")
    pygame.quit()