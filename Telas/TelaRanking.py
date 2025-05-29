import pygame
import os
from interfaces.database import Database # Importa a CLASSE Database

class RankingTela:
    def __init__(self,tela_principal=None):
        self.tela_principal = tela_principal
        self.largura_da_tela = 1280
        self.altura_da_tela = 720
        self.tela_ranking = pygame.Surface((self.largura_da_tela, self.altura_da_tela))
        self.rect_tela_ranking = self.tela_ranking.get_rect(center=self.tela_principal.get_rect().center)

        self.ranking_data = []

        # Instancia a classe Database para gerenciar as operações de DB
        self.db_manager = Database() 
        # É uma boa prática conectar aqui, ou no início do programa principal,
        # e fechar a conexão quando o programa terminar.
        self.db_manager.connect() # Conecta ao banco de dados ao inicializar a tela de ranking

        self.margem = 10
        self.altura_cabecalho = 40
        self.espacamento_cabecalho = 5
        self.largura_coluna_nome = (self.largura_da_tela - 3 * self.espacamento_cabecalho - 2 * self.margem) // 4
        self.largura_coluna_email = self.largura_coluna_nome
        self.largura_coluna_pontuacao = self.largura_coluna_nome
        self.largura_coluna_materia = self.largura_coluna_nome
        
        self.rects_cabecalho = []
        x_atual = self.margem
        for texto in ["NOME DO ALUNO", "EMAIL DO ALUNO", "PONTUAÇÃO", "MATÉRIA"]:
            if texto == "EMAIL DO ALUNO":
                largura = self.largura_coluna_email
            elif texto == "PONTUAÇÃO":
                largura = self.largura_coluna_pontuacao
            else: # MATÉRIA
                largura = self.largura_coluna_materia
            
            rect = pygame.Rect(
                x_atual,
                self.margem,
                largura,
                self.altura_cabecalho
            )
            self.rects_cabecalho.append((rect, texto))
            x_atual += largura + self.espacamento_cabecalho

        self.altura_linha = 30
        self.espacamento_linha = 5
        self.margem_topo_lista = self.margem + self.altura_cabecalho + 2 * self.espacamento_cabecalho

        self.largura_botao_fechar = 80
        self.altura_botao_fechar = 25
        self.rect_botao_fechar = pygame.Rect(
            self.largura_da_tela - self.margem - self.largura_botao_fechar,
            self.altura_da_tela - self.margem - self.altura_botao_fechar,
            self.largura_botao_fechar,
            self.altura_botao_fechar
        )

        self.carregar_dados_ranking()

    def carregar_dados_ranking(self):
        """Carrega os dados do ranking do banco de dados e formata para exibição."""
        # Chama o método get_rank_partidas da instância db_manager
        dados_brutos = self.db_manager.get_rank_partidas()
        self.ranking_data = []
        for email,nome, pontuacao, materia in dados_brutos:
            self.ranking_data.append({
                "email": email,
                "nome": nome,
                "pontuacao": str(pontuacao),
                "materia": materia
            })

    def desenhar_texto_centralizado(self, tela, texto, tamanho_fonte, cor, rect):
        fonte = pygame.font.Font(None, tamanho_fonte)
        surf = fonte.render(texto, True, cor)
        texto_rect = surf.get_rect(center=rect.center)
        tela.blit(surf, texto_rect)

    def desenhar_cabecalhos(self):
        cor_fundo = pygame.Color("dimgray")
        cor_texto = pygame.Color("white")
        for rect, texto in self.rects_cabecalho:
            pygame.draw.rect(self.tela_ranking, cor_fundo, rect, border_radius=3)
            self.desenhar_texto_centralizado(self.tela_ranking, texto, 22, cor_texto, rect)

    def desenhar_botao_fechar(self):
        cor_botao = pygame.Color("saddlebrown")
        cor_texto = pygame.Color("white")
        pygame.draw.rect(self.tela_ranking, cor_botao, self.rect_botao_fechar, border_radius=3)
        self.desenhar_texto_centralizado(self.tela_ranking, "FECHAR", 20, cor_texto, self.rect_botao_fechar)

    def desenhar_ranking_data(self):
        y = self.margem_topo_lista
        cor_linha_fundo = pygame.Color(100, 100, 100, 150) 
        cor_texto = pygame.Color("white")
        fonte = pygame.font.Font(None, 28) 

        for data in self.ranking_data:
            pygame.draw.rect(
                self.tela_ranking,
                cor_linha_fundo,
                (self.margem, y, self.largura_da_tela - 2 * self.margem, self.altura_linha),
                border_radius=2
            )


            x_nome = self.margem + 5
            x_email = x_nome + self.largura_coluna_nome + self.espacamento_cabecalho
            x_pontuacao = x_email + self.largura_coluna_email + self.espacamento_cabecalho
            x_materia = x_pontuacao + self.largura_coluna_pontuacao + self.espacamento_cabecalho

            surf_nome = fonte.render(data["nome"], True, cor_texto)
            self.tela_ranking.blit(surf_nome, (x_nome, y + (self.altura_linha - surf_nome.get_height()) // 2))

            surf_email = fonte.render(data["email"], True, cor_texto)
            self.tela_ranking.blit(surf_email, (x_email, y + (self.altura_linha - surf_email.get_height()) // 2))

            surf_pontuacao = fonte.render(data["pontuacao"], True, cor_texto)
            self.tela_ranking.blit(surf_pontuacao, (x_pontuacao, y + (self.altura_linha - surf_pontuacao.get_height()) // 2))

            surf_materia = fonte.render(data["materia"], True, cor_texto)
            self.tela_ranking.blit(surf_materia, (x_materia, y + (self.altura_linha - surf_materia.get_height()) // 2))


            y += self.altura_linha + self.espacamento_linha

    def executar(self):
        """Exibe a tela de ranking e gerencia os eventos."""
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    # Close the database connection when exiting
                    self.db_manager.close()
                    return False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    pos_rel = (pos[0] - self.rect_tela_ranking.left, pos[1] - self.rect_tela_ranking.top)
                    if self.rect_botao_fechar.collidepoint(pos_rel):
                        # Close the database connection when closing the ranking screen
                        self.db_manager.close()
                        return True

            self.tela_ranking.fill(pygame.Color("lightgray"))
            self.desenhar_cabecalhos()
            self.desenhar_botao_fechar()
            self.desenhar_ranking_data()
            
            self.tela_principal.blit(self.tela_ranking, self.rect_tela_ranking)
            pygame.display.flip()
        
        # Ensure connection is closed even if loop exits unexpectedly
        self.db_manager.close()
        return True


if __name__ == '__main__':
    pygame.init()
    tela_principal = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Ranking de Partidas")

    ranking_tela = RankingTela(tela_principal)
    ranking_tela.executar()

    pygame.quit()