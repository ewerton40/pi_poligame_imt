import pygame
from .elementos_visuais import Cores, Fonte, desenhar_texto_centralizado

class RankingTela:
    def __init__(self, tela_principal, ranking_data):
        self.tela_principal = tela_principal
        self.largura_da_tela = 800
        self.altura_da_tela = 600
        self.tela_ranking = pygame.Surface((self.largura_da_tela, self.altura_da_tela))
        self.rect_tela_ranking = self.tela_ranking.get_rect(center=self.tela_principal.get_rect().center)
        self.margem = 10
        self.altura_cabecalho = 40
        self.espacamento_cabecalho = 5
        self.largura_coluna = (self.largura_da_tela - 2 * self.margem - 3 * self.espacamento_cabecalho) // 4
        self.altura_linha = 30
        self.espacamento_linha = 5
        self.margem_topo_lista = self.margem + self.altura_cabecalho + 2 * self.espacamento_cabecalho
        self.ranking_data = ranking_data
        self.rect_nome = pygame.Rect(self.margem, self.margem, self.largura_coluna, self.altura_cabecalho)
        self.rect_pontuacao = pygame.Rect(self.margem + self.largura_coluna + self.espacamento_cabecalho, self.margem, self.largura_coluna, self.altura_cabecalho)
        self.rect_identificacao = pygame.Rect(self.margem + 2 * (self.largura_coluna + self.espacamento_cabecalho), self.margem, self.largura_coluna, self.altura_cabecalho)
        self.rect_turma = pygame.Rect(self.margem + 3 * (self.largura_coluna + self.espacamento_cabecalho), self.margem, self.largura_coluna, self.altura_cabecalho)
        self.largura_botao_fechar = 80
        self.altura_botao_fechar = 25
        self.rect_botao_fechar = pygame.Rect(self.largura_da_tela - self.margem - self.largura_botao_fechar, self.altura_da_tela - self.margem - self.altura_botao_fechar, self.largura_botao_fechar, self.altura_botao_fechar)

    def desenhar_cabecalhos(self):
        pygame.draw.rect(self.tela_ranking, Cores.CABECALHO, self.rect_nome, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "NOME", Fonte.CABECALHO, Cores.TEXTO_CABECALHO, self.rect_nome)
        pygame.draw.rect(self.tela_ranking, Cores.CABECALHO, self.rect_pontuacao, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "PONTUAÇÃO", Fonte.CABECALHO, Cores.TEXTO_CABECALHO, self.rect_pontuacao)
        pygame.draw.rect(self.tela_ranking, Cores.CABECALHO, self.rect_identificacao, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "IDENTIFICAÇÃO", Fonte.CABECALHO, Cores.TEXTO_CABECALHO, self.rect_identificacao)
        pygame.draw.rect(self.tela_ranking, Cores.CABECALHO, self.rect_turma, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "TURMA", Fonte.CABECALHO, Cores.TEXTO_CABECALHO, self.rect_turma)

    def desenhar_botao_fechar(self):
        pygame.draw.rect(self.tela_ranking, Cores.BOTAO_FECHAR, self.rect_botao_fechar, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "FECHAR", Fonte.FECHAR, Cores.TEXTO_FECHAR, self.rect_botao_fechar)

    def desenhar_ranking_data(self):
        y_linha = self.margem_topo_lista
        for data in self.ranking_data:
            pygame.draw.rect(self.tela_ranking, Cores.LINHA, (self.margem, y_linha, self.largura_da_tela - 2 * self.margem, self.altura_linha), border_radius=2)
            texto_nome = Fonte.PADRAO.render(data["nome"], True, Cores.TEXTO)
            self.tela_ranking.blit(texto_nome, (self.margem + 5, y_linha + self.altura_linha // 2 - texto_nome.get_height() // 2))
            texto_pontuacao = Fonte.PADRAO.render(data["pontuacao"], True, Cores.TEXTO)
            self.tela_ranking.blit(texto_pontuacao, (self.rect_pontuacao.left + 5, y_linha + self.altura_linha // 2 - texto_pontuacao.get_height() // 2))
            texto_identificacao = Fonte.PADRAO.render(data["identificacao"], True, Cores.TEXTO)
            self.tela_ranking.blit(texto_identificacao, (self.rect_identificacao.left + 5, y_linha + self.altura_linha // 2 - texto_identificacao.get_height() // 2))
            texto_turma = Fonte.PADRAO.render(data["turma"], True, Cores.TEXTO)
            self.tela_ranking.blit(texto_turma, (self.rect_turma.left + 5, y_linha + self.altura_linha // 2 - texto_turma.get_height() // 2))
            y_linha += self.altura_linha + self.espacamento_linha

    def exibir(self):
        rodando_ranking = True
        while rodando_ranking:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando_ranking = False
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    pos_mouse_ranking = (pos_mouse[0] - self.rect_tela_ranking.left, pos_mouse[1] - self.rect_tela_ranking.top)
                    if self.rect_botao_fechar.collidepoint(pos_mouse_ranking):
                        rodando_ranking = False
                        return True

            self.tela_ranking.fill(Cores.FUNDO)
            self.desenhar_cabecalhos()
            self.desenhar_botao_fechar()
            self.desenhar_ranking_data()
            self.tela_principal.blit(self.tela_ranking, self.rect_tela_ranking)
            pygame.display.flip()
        return True

# A função abrir_janela2 NÃO deve estar aqui
# def abrir_janela2(tela_principal):
#     """Cria e exibe a janela de ranking adaptada para 800x600."""
#     ranking_data = [...]
#     ranking_tela = RankingTela(tela_principal, ranking_data)
#     return ranking_tela.exibir()

if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tela de Ranking Teste")
    ranking_data_teste = [
        {"nome": "Teste 1", "pontuacao": "$100", "identificacao": "T1", "turma": "A"},
        {"nome": "Teste 2", "pontuacao": "$200", "identificacao": "T2", "turma": "B"}
    ]
    ranking = RankingTela(tela_teste, ranking_data_teste)
    ranking.exibir()
    pygame.quit()