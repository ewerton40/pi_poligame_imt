import pygame
from Classes.rankingAlunos import RankingTela

class TelaRanking:
    def __init__(self, tela_principal):
        self.tela_principal = tela_principal
        self.ranking_data = [
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
        self.ranking_tela = RankingTela(self.tela_principal, self.ranking_data)

    def executar(self):
        """Exibe a tela de ranking e retorna quando fechar."""
        return self.ranking_tela.exibir()


if __name__ == '__main__':
    pygame.init()
    tela_teste = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tela de Ranking Teste")

    ranking = TelaRanking(tela_teste)
    ranking.executar()

    pygame.quit()
