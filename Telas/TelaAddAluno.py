import pygame
from Telas.Tela import Tela
from UI.Botao import Botao
from interfaces.database import Database  # Sua classe de banco de dados
import sys # Importe sys para um tratamento de saída mais elegante
from interfaces.database import Database

# Instância global do banco de dados
db = Database()
db.connect() # Conecta ao banco de dados uma vez na inicialização do programa

class AddPerguntaTela:
    def __init__(self):
        self.largura, self.altura = 1280, 720
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Adicionar Pergunta")

        self.margem = 20
        self.fonte_30 = pygame.font.Font(None, 30)
        self.fonte_24 = pygame.font.Font(None, 24)

        self.label_pergunta = self.fonte_30.render("PERGUNTA", True, pygame.Color("white"))
        self.rect_label = self.label_pergunta.get_rect(topleft=(self.margem, self.margem))

        self.caixatexto = pygame.Rect(self.margem, self.rect_label.bottom + 10, 400, 100)
        self.texto_pergunta = ""
        self.ativo_pergunta = False

        self.rects_alt = [pygame.Rect(self.margem, self.caixatexto.bottom + 20 + i * 50,
                                        self.caixatexto.width, 40) for i in range(4)]
        self.textos_alt = [""] * 4
        self.ativos_alt = [False] * 4

        # Adicionar uma forma de indicar qual alternativa é a correta
        # Vamos usar um índice para a alternativa correta
        self.indice_alternativa_correta = -1 # -1 significa nenhuma selecionada
        self.circulos_correta = [
            pygame.Rect(r.right + 10, r.centery - 10, 20, 20) for r in self.rects_alt
        ]


        bw, bh, esp = 120, 40, 10
        x_lat = self.largura - self.margem - bw
        self.rect_add = pygame.Rect(x_lat, self.margem, bw, bh)
        self.rect_cancel = pygame.Rect(x_lat, self.margem + bh + esp, bw, bh)

        self.rect_filt = pygame.Rect(self.margem, self.altura - self.margem - 30, 100, 30)
        
        # Mapeamento de nomes de matéria para IDs (em um app real, viria do DB)
        # Você pode usar db.get_questao_materia() para popular isso dinamicamente
        self.materias_db = {
            "história": 1,
            "matemática": 2,
            "física": 3,
            "química": 4,
            "biologia": 5,
            "geometria": 6,
            "português": 7,
            "literatura": 8
            # Adicione mais conforme seus IDs de matéria
        }
        self.dificuldades_validas = ["fácil", "médio", "difícil"]

        self.filtros = list(self.dificuldades_validas) + list(self.materias_db.keys())
        self.sel_filtros = [] # Guarda os nomes dos filtros selecionados
        self.mostrar = False
        self.rect_box = pygame.Rect(self.rect_filt.x, self.rect_filt.y - len(self.filtros) * 30 - 10,
                                        200, len(self.filtros) * 30 + 10)
        self.rects_filt = [pygame.Rect(self.rect_box.x + 5, self.rect_box.y + 5 + i * 30,
                                        self.rect_box.width - 10, 25) for i in range(len(self.filtros))]
        
        # Variáveis para armazenar a dificuldade e matéria selecionadas para adicionar a questão
        self.dificuldade_selecionada = None
        self.id_materia_selecionada = None

    def desenhar_texto_centralizado(self, texto, fonte, cor, rect):
        surf = fonte.render(texto, True, cor)
        texto_rect = surf.get_rect(center=rect.center)
        self.tela.blit(surf, texto_rect)

    def executar(self):
        rodando = True
        retorno = "cancelar"

        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    retorno = "fechar_janela"
                    db.disconnect() # Desconecta ao sair
                    pygame.quit()
                    sys.exit()

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    # Lógica para mostrar/esconder filtros
                    if self.mostrar and not self.rect_box.collidepoint(pos):
                        self.mostrar = False
                    if self.rect_filt.collidepoint(pos):
                        self.mostrar = not self.mostrar

                    # Ativar caixa de texto de pergunta
                    if self.caixatexto.collidepoint(pos):
                        self.ativo_pergunta = True
                        self.ativos_alt = [False] * 4
                    else:
                        self.ativo_pergunta = False
                        # Ativar caixas de texto de alternativas
                        for i, r in enumerate(self.rects_alt):
                            if r.collidepoint(pos):
                                self.ativos_alt = [False] * 4
                                self.ativos_alt[i] = True
                                break
                        else: # Se não clicou em nenhuma caixa de alternativa
                            self.ativos_alt = [False] * 4

                    # Lógica para seleção da alternativa correta (círculos)
                    for i, circle_rect in enumerate(self.circulos_correta):
                        if circle_rect.collidepoint(pos):
                            self.indice_alternativa_correta = i
                            break
                    
                    # Clicks nos botões
                    if self.rect_add.collidepoint(pos):
                        enunciado = self.texto_pergunta.strip()
                        # Dificuldade e Matéria
                        dificuldade_sel = None
                        materia_sel = None
                        
                        # Extrai dificuldade e matéria dos filtros selecionados
                        for f in self.sel_filtros:
                            if f in self.dificuldades_validas:
                                if dificuldade_sel: # Garante que apenas uma dificuldade é selecionada
                                    print("Selecione apenas uma dificuldade (fácil, médio, difícil).")
                                    return # Ou mostre um erro ao usuário
                                dificuldade_sel = f
                            elif f in self.materias_db:
                                if materia_sel: # Garante que apenas uma matéria é selecionada
                                    print("Selecione apenas uma matéria.")
                                    return # Ou mostre um erro ao usuário
                                materia_sel = f
                        
                        if not enunciado:
                            print("O enunciado da pergunta não pode estar vazio.")
                        elif not dificuldade_sel:
                            print("Selecione a dificuldade da pergunta (fácil, médio, difícil).")
                        elif not materia_sel:
                            print("Selecione a matéria da pergunta.")
                        elif any(not alt.strip() for alt in self.textos_alt):
                            print("Todas as 4 alternativas devem ser preenchidas.")
                        elif self.indice_alternativa_correta == -1:
                            print("Selecione a alternativa correta.")
                        else:
                            # Prepara os dados para o db.add_questao
                            alter1 = self.textos_alt[0].strip()
                            alter2 = self.textos_alt[1].strip()
                            alter3 = self.textos_alt[2].strip()
                            answer = self.textos_alt[self.indice_alternativa_correta].strip() # A resposta correta

                            # Ajusta as alternativas para passar para add_questao
                            # Garante que 'answer' é a alternativa marcada como correta
                            # E as outras são as 'alterN'
                            todas_alternativas = list(self.textos_alt)
                            alternativas_para_db = []
                            for i, alt_texto in enumerate(todas_alternativas):
                                if i == self.indice_alternativa_correta:
                                    # Esta é a resposta correta, a tratamos como 'answer' no método add_questao
                                    pass # Não adicionamos aqui, será o último parâmetro
                                else:
                                    alternativas_para_db.append(alt_texto.strip())

                            # Certifique-se de que há 3 alternativas erradas e 1 correta
                            if len(alternativas_para_db) != 3:
                                print("Erro interno: Problema na coleta das alternativas.")
                                continue # Pula para o próximo loop

                            # Mapear nome da matéria para ID
                            id_materia = self.materias_db.get(materia_sel)

                            print(f"Tentando adicionar questão: Enunciado='{enunciado}', Dificuldade='{dificuldade_sel}', Matéria ID={id_materia}")
                            print(f"Alternativas: Errada1='{alternativas_para_db[0]}', Errada2='{alternativas_para_db[1]}', Errada3='{alternativas_para_db[2]}', Correta='{answer}'")

                            # CHAMA O MÉTODO DA CLASSE DATABASE AQUI
                            sucesso = db.add_questao(
                                Enunciado=enunciado,
                                DificuldadePergunta=dificuldade_sel,
                                idMateria=id_materia,
                                alter1=alternativas_para_db[0], # A primeira alternativa errada
                                alter2=alternativas_para_db[1], # A segunda alternativa errada
                                alter3=alternativas_para_db[2], # A terceira alternativa errada
                                answer=answer # A alternativa correta
                            )

                            if sucesso:
                                print("Questão adicionada com sucesso!")
                                retorno = "questao_adicionada"
                                rodando = False
                            else:
                                print("Falha ao adicionar questão. Verifique o console para erros do banco.")
                                retorno = "erro_adicionar_questao"
                                # Você pode querer manter a tela aberta em caso de erro, ou fechar
                                # rodando = False

                    elif self.rect_cancel.collidepoint(pos):
                        print("Adição de pergunta cancelada.")
                        rodando = False
                        retorno = "cancelar"

                    # Lógica para cliques nos filtros (dificuldade/matéria)
                    if self.mostrar:
                        for i, r in enumerate(self.rects_filt):
                            if r.collidepoint(pos):
                                f = self.filtros[i]
                                if f in self.sel_filtros:
                                    self.sel_filtros.remove(f)
                                    # Limpa a seleção se desmarcou
                                    if f in self.dificuldades_validas:
                                        self.dificuldade_selecionada = None
                                    elif f in self.materias_db:
                                        self.id_materia_selecionada = None
                                else:
                                    # Adiciona o filtro e atualiza as variáveis de seleção
                                    if f in self.dificuldades_validas:
                                        # Garante que apenas uma dificuldade pode ser selecionada
                                        for d in self.dificuldades_validas:
                                            if d in self.sel_filtros:
                                                self.sel_filtros.remove(d)
                                        self.dificuldade_selecionada = f
                                    elif f in self.materias_db:
                                        # Garante que apenas uma matéria pode ser selecionada
                                        for m in self.materias_db.keys():
                                            if m in self.sel_filtros:
                                                self.sel_filtros.remove(m)
                                        self.id_materia_selecionada = self.materias_db[f]
                                    
                                    self.sel_filtros.append(f)
                                break # Sai do loop de filtros após um clique

                elif evento.type == pygame.KEYDOWN:
                    if self.ativo_pergunta:
                        if evento.key == pygame.K_BACKSPACE:
                            self.texto_pergunta = self.texto_pergunta[:-1]
                        elif evento.key == pygame.K_TAB:
                            self.ativo_pergunta = False
                            self.ativos_alt[0] = True # Ativa a primeira alternativa
                        elif evento.key != pygame.K_RETURN:
                            self.texto_pergunta += evento.unicode
                    else:
                        for i, ativo in enumerate(self.ativos_alt):
                            if ativo:
                                if evento.key == pygame.K_BACKSPACE:
                                    self.textos_alt[i] = self.textos_alt[i][:-1]
                                elif evento.key == pygame.K_TAB:
                                    self.ativos_alt[i] = False
                                    next_index = (i + 1) % len(self.ativos_alt)
                                    self.ativos_alt[next_index] = True
                                elif evento.key != pygame.K_RETURN:
                                    self.textos_alt[i] += evento.unicode
                                break # Processa apenas a caixa ativa

            # --- Desenho ---
            self.tela.fill(pygame.Color("black"))
            self.tela.blit(self.label_pergunta, self.rect_label)

            cor_bg = pygame.Color("dimgray")
            cor_border = pygame.Color("dodgerblue") if self.ativo_pergunta else pygame.Color("gray")
            self.tela.fill(cor_bg, self.caixatexto)
            pygame.draw.rect(self.tela, cor_border, self.caixatexto, 2, border_radius=5)
            surf = self.fonte_30.render(self.texto_pergunta, True, pygame.Color("white"))
            self.tela.blit(surf, (self.caixatexto.x + 5, self.caixatexto.y + 5))

            for i, r in enumerate(self.rects_alt):
                cor_b = pygame.Color("dodgerblue") if self.ativos_alt[i] else pygame.Color("gray")
                self.tela.fill(cor_bg, r)
                pygame.draw.rect(self.tela, cor_b, r, 2, border_radius=5)
                rot = self.fonte_24.render(f"{chr(65 + i)}.", True, pygame.Color("white"))
                self.tela.blit(rot, (r.x - 30, r.y + 5))
                text = self.fonte_30.render(self.textos_alt[i], True, pygame.Color("white"))
                self.tela.blit(text, (r.x + 10, r.y + 5))

                # Desenha o círculo para marcar a alternativa correta
                circle_color = pygame.Color("green") if self.indice_alternativa_correta == i else pygame.Color("red")
                pygame.draw.circle(self.tela, circle_color, self.circulos_correta[i].center, self.circulos_correta[i].width // 2, 2)
                if self.indice_alternativa_correta == i:
                     # Desenha um ponto verde se for a correta
                    pygame.draw.circle(self.tela, pygame.Color("green"), self.circulos_correta[i].center, self.circulos_correta[i].width // 2 - 4)


            for rect, txt in [(self.rect_add, "ADICIONAR"),
                                (self.rect_cancel, "CANCELAR"),
                                (self.rect_filt, "FILTROS")]:
                cor_btn = pygame.Color("saddlebrown")
                self.tela.fill(cor_btn, rect)
                self.desenhar_texto_centralizado(txt, self.fonte_24, pygame.Color("white"), rect)

            if self.mostrar:
                self.tela.fill(cor_bg, self.rect_box)
                pygame.draw.rect(self.tela, pygame.Color("gray"), self.rect_box, 2, border_radius=5)
                for i, (f, r) in enumerate(zip(self.filtros, self.rects_filt)):
                    bg = pygame.Color("darkgreen") if f in self.sel_filtros else pygame.Color("darkred")
                    self.tela.fill(bg, r)
                    text = self.fonte_24.render(f, True, pygame.Color("white"))
                    self.tela.blit(text, (r.x + 5, r.y + 5))

            pygame.display.flip()

        return retorno


if __name__ == '__main__':
    pygame.init()
    # Para testar AddPerguntaTela, você precisa de uma tela principal válida.
    # No seu código original, ela é 'tela_principal'.
    # Aqui, simulamos isso para o teste direto.
    tela_simulada = pygame.display.set_mode((1280, 720)) # Adapte ao tamanho da sua tela
    
    app = AddPerguntaTela()
    resultado = app.executar()
    print("Resultado da adição de pergunta:", resultado)
    
    db.disconnect() # Garante que a conexão seja fechada ao final do programa principal
    pygame.quit()
    sys.exit()

# É uma boa prática fechar a conexão com o banco de dados quando o programa termina.
# Isso pode ser feito no seu loop principal do jogo, ou de forma mais robusta
# usando um gerenciador de contexto se você estiver usando uma abordagem de "with" para a conexão,
# ou simplesmente chamando db.disconnect() antes de pygame.quit() no loop principal.
# Se você tiver um gerenciador de estados de tela, pode chamar db.disconnect() ao finalizar o programa.
# No exemplo acima, adicionei a chamada em QUIT.