# Arquivo: adicionarAluno.py
import pygame
from Classes.elementos_visuais import Cores, Fonte
from Classes.componentes import criar_caixa_texto, desenhar_caixa_texto, criar_botao, desenhar_botao

def abrir_tela_adicionar_aluno(tela):
    """Função para criar e exibir a tela de adicionar aluno."""
    largura_tela = 800
    altura_tela = 600
    tela_adicionar = pygame.Surface((largura_tela, altura_tela))
    tela_adicionar.fill(Cores.FUNDO)
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
        tela_adicionar.fill(Cores.FUNDO)

        for caixa in caixas_texto:
            desenhar_caixa_texto(tela_adicionar, caixa)

        for botao in botoes:
            desenhar_botao(tela_adicionar, botao)

        tela.blit(tela_adicionar, (0, 0))  # Blita a superfície na tela principal
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                retorno = "fechar_janela"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                pos_mouse_local = (pos_mouse[0], pos_mouse[1]) # Mouse na tela adicionar

                for i, caixa in enumerate(caixas_texto):
                    if caixa["rect"].collidepoint(pos_mouse_local):
                        caixa["ativo"] = True
                    else:
                        caixa["ativo"] = False

                if botao_adicionar["rect"].collidepoint(pos_mouse_local):
                    email = caixa_email["texto"]
                    senha = caixa_senha["texto"]
                    print(f"Adicionar Aluno - Email: {email}, Senha: {senha}")
                    retorno = "adicionar_aluno" # Sinaliza que o botão adicionar foi clicado
                    rodando = False
                elif botao_cancelar["rect"].collidepoint(pos_mouse_local):
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

    return retorno

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    tela_teste = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Teste Adicionar Aluno")
    resultado = abrir_tela_adicionar_aluno(tela_teste)
    print(f"Resultado da tela de adicionar aluno: {resultado}")
    pygame.quit()