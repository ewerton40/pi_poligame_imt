import pygame
import Constantes   
from UI.Botao import Botao
from hashlib import sha256
from Telas.TelaInicio import TelaInicio
from Telas.TelaGerenciamento import TelaGerenciamento

class TelaLogin:
    def __init__(self, screen, transition_call, quit_game, database):
        self.screen = screen
        self.transition_call = transition_call
        self.quit = quit_game
        self.database = database
        self.is_loaded = False

        # Configurações de fonte
        self.fonte_pequena = pygame.font.SysFont("Arial", 20)
        self.fonte_media = pygame.font.SysFont("Arial", 24)
        self.fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
        self.fonte_colegio = pygame.font.SysFont("Arial", 28, italic=True)

        # Elementos da interface
        self.botao_entrar = Botao(
            (Constantes.largura // 2 - -300, 450),
            (200, 50),
            pygame.Color("dodgerblue"),
            "Entrar",
            self.fonte_media
        )

        # Campos de entrada
        self.campos = {
            "usuario": {
                "retangulo": pygame.Rect(Constantes.largura // 2 - -200, 315, 400, 40),
                "texto": "",
                "ativo": False,
                "rotulo": "Usuário:",
                "senha": False
            },
            "senha": {
                "retangulo": pygame.Rect(Constantes.largura // 2 - -200, 380, 400, 40),
                "texto": "",
                "ativo": False,
                "rotulo": "Senha:",
                "senha": True
            }
        }

        # Estado da tela
        self.mensagem_erro = "Usuario não encontrado"
        self.cor_erro = pygame.Color(200, 0, 0)
        self.cor_fundo = pygame.Color(240, 240, 240)
        self.cor_titulo = pygame.Color(30, 30, 30)
        self.cor_texto = pygame.Color(50, 50, 50)

        # Posição fixa para a mensagem de erro
        self.posicao_erro = (850, 420)

    def load(self):
        self.images = {
            "background": pygame.image.load("imagens/tela_login.png").convert(),
        }
        self.is_loaded = all(image is not None for image in self.images.values())

    def run(self, events):
        if self.is_loaded:
            self.screen.fill(self.cor_fundo)
            self.screen.blit(self.images["background"], (0, 0))

            # Desenha campos de entrada
            for campo in self.campos.values():
                self.desenhar_campo(campo)

            # Desenha botão e mensagens
            self.botao_entrar.draw(self.screen)
            self.mostrar_mensagem_erro()

            # Processa eventos
            self.tratar_eventos(events)

            # Verifica ação do botão
            if self.botao_entrar.check_button():
                self.verificar_login()

    def desenhar_campo(self, campo):
        cor_fundo = "dodgerblue" if campo["ativo"] else "lightgray"
        pygame.draw.rect(self.screen, pygame.Color(cor_fundo), campo["retangulo"], 0, border_radius=5)
        pygame.draw.rect(self.screen, pygame.Color("black"), campo["retangulo"], 2, border_radius=5)

        # Rótulo
        texto_rotulo = self.fonte_pequena.render(campo["rotulo"], True, self.cor_texto)
        self.screen.blit(texto_rotulo, (campo["retangulo"].x, campo["retangulo"].y - 25))

        # Texto digitado
        texto = "*" * len(campo["texto"]) if campo["senha"] else campo["texto"]
        texto_surface = self.fonte_pequena.render(texto, True, "black")
        self.screen.blit(texto_surface, (campo["retangulo"].x + 10, campo["retangulo"].y + 10))

    def mostrar_mensagem_erro(self):
        if self.mensagem_erro:
            erro = self.fonte_pequena.render(self.mensagem_erro, True, self.cor_erro)
            self.screen.blit(erro, self.posicao_erro)  # Posição definida por self.posicao_erro

    def tratar_eventos(self, events):
         for event in events:
            if event.type == pygame.QUIT:
                self.quit()

            # Clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.processar_clique(event.pos)

            # Teclado
            if event.type == pygame.KEYDOWN:
                self.processar_tecla(event)

    def processar_clique(self, pos):
        for nome, campo in self.campos.items():
            campo["ativo"] = False

        for nome, campo in self.campos.items():
            if campo["retangulo"].collidepoint(pos):
                campo["ativo"] = True
                break

        # Limpa mensagem de erro ao interagir
        self.mensagem_erro = ""

    def processar_tecla(self, event):
        print("Tecla pressionada:", event.unicode, event.key)
        for nome, campo in self.campos.items():
            if campo["ativo"]:
                print(f"Campo ativo: {nome}")
                if event.key == pygame.K_BACKSPACE:
                    campo["texto"] = campo["texto"][:-1]
                elif event.key == pygame.K_RETURN:
                    self.verificar_login()
                else:
                    if event.unicode.isprintable():
                        campo["texto"] += event.unicode

    def verificar_login(self):
        email = self.campos["usuario"]["texto"]
        senha = self.campos["senha"]["texto"]

        if not email or not senha:
            self.mensagem_erro = "Preencha todos os campos!"
            return

        senha_hash = sha256(senha.encode("utf-8")).hexdigest()

        user = self.database.login_usuario(email, senha_hash)
        if user:
            if user["tipo"] == "Professor":
                self.transition_call(TelaGerenciamento(self.screen, self.transition_call))  # ou sua tela de professor
            elif user["tipo"] == "Aluno":
                self.transition_call(TelaInicio(self.screen, self.transition_call, user_data=user))

        else:
            self.mensagem_erro = "Credenciais inválidas!"