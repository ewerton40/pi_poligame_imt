import pygame

# Fontes locais
FONTE_PADRAO = pygame.font.Font(None, 30)
FONTE_CABECALHO = pygame.font.Font(None, 22)
FONTE_FECHAR = pygame.font.Font(None, 20)

# Função auxiliar para desenhar texto centralizado
def desenhar_texto_centralizado(tela, texto, fonte, cor, rect):
    surf = fonte.render(texto, True, cor)
    texto_rect = surf.get_rect(center=rect.center)
    tela.blit(surf, texto_rect)

class RankingTela:
    def __init__(self, tela_principal, ranking_data):
        self.tela_principal = tela_principal
        self.largura_da_tela = 800
        self.altura_da_tela = 600
        self.tela_ranking = pygame.Surface((self.largura_da_tela, self.altura_da_tela))
        self.rect_tela_ranking = self.tela_ranking.get_rect(center=self.tela_principal.get_rect().center)

        # Layout de colunas
        self.margem = 10
        self.altura_cabecalho = 40
        self.espacamento_cabecalho = 5
        total_espaco = 3 * self.espacamento_cabecalho + 2 * self.margem
        self.largura_coluna = (self.largura_da_tela - total_espaco) // 4

        # Linhas de dados
        self.altura_linha = 30
        self.espacamento_linha = 5
        self.margem_topo_lista = self.margem + self.altura_cabecalho + 2 * self.espacamento_cabecalho

        # Retângulos de cabeçalho
        x0 = self.margem
        offsets = [0, 1, 2, 3]
        self.rects_cabecalho = []
        for i, texto in zip(offsets, ["NOME", "PONTUAÇÃO", "IDENTIFICAÇÃO", "TURMA"]):
            rect = pygame.Rect(
                x0 + i * (self.largura_coluna + self.espacamento_cabecalho),
                self.margem,
                self.largura_coluna,
                self.altura_cabecalho
            )
            self.rects_cabecalho.append((rect, texto))

        # Botão fechar
        self.largura_botao_fechar = 80
        self.altura_botao_fechar = 25
        self.rect_botao_fechar = pygame.Rect(
            self.largura_da_tela - self.margem - self.largura_botao_fechar,
            self.altura_da_tela - self.margem - self.altura_botao_fechar,
            self.largura_botao_fechar,
            self.altura_botao_fechar
        )

        self.ranking_data = ranking_data

    def desenhar_cabecalhos(self):
        cor_fundo = pygame.Color("dimgray")
        cor_texto = pygame.Color("white")
        for rect, texto in self.rects_cabecalho:
            pygame.draw.rect(self.tela_ranking, cor_fundo, rect, border_radius=3)
            desenhar_texto_centralizado(self.tela_ranking, texto, FONTE_CABECALHO, cor_texto, rect)

    def desenhar_botao_fechar(self):
        cor_botao = pygame.Color("saddlebrown")
        cor_texto = pygame.Color("white")
        pygame.draw.rect(self.tela_ranking, cor_botao, self.rect_botao_fechar, border_radius=3)
        desenhar_texto_centralizado(self.tela_ranking, "FECHAR", FONTE_FECHAR, cor_texto, self.rect_botao_fechar)

    def desenhar_ranking_data(self):
        y = self.margem_topo_lista
        cor_linha = pygame.Color("gray")
        cor_texto = pygame.Color("white")
        for data in self.ranking_data:
            # Desenha fundo da linha
            pygame.draw.rect(
                self.tela_ranking,
                cor_linha,
                (self.margem, y, self.largura_da_tela - 2 * self.margem, self.altura_linha),
                border_radius=2
            )
            # Desenha colunas de texto
            textos = [data["nome"], data["pontuacao"], data["identificacao"], data["turma"]]
            for i, texto in enumerate(textos):
                surf = FONTE_PADRAO.render(texto, True, cor_texto)
                x = self.margem + i * (self.largura_coluna + self.espacamento_linha) + 5
                y_texto = y + (self.altura_linha - surf.get_height()) // 2
                self.tela_ranking.blit(surf, (x, y_texto))
            y += self.altura_linha + self.espacamento_linha

    def exibir(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos_rel = (pos[0] - self.rect_tela_ranking.left, pos[1] - self.rect_tela_ranking.top)
                    if self.rect_botao_fechar.collidepoint(pos_rel):
                        return True

            # Fundo geral
            self.tela_ranking.fill(pygame.Color("lightgray"))
            self.desenhar_cabecalhos()
            self.desenhar_botao_fechar()
            self.desenhar_ranking_data()
            self.tela_principal.blit(self.tela_ranking, self.rect_tela_ranking)
            pygame.display.flip()
        return True

if __name__ == '__main__':
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tela de Ranking Teste")
    dados = [
        {"nome": "Teste 1", "pontuacao": "100", "identificacao": "T1", "turma": "A"},
        {"nome": "Teste 2", "pontuacao": "200", "identificacao": "T2", "turma": "B"}
    ]
    ranking = RankingTela(tela, dados)
    ranking.exibir()
    pygame.quit()
