import pygame
import sys
import os
import sys
import Constantes
import sys    
from  Telas import TelaAdmin

import sys
from pathlib import Path
from Botao import Botao

class TelaLogin:
    def __init__(self, screen, transition_call, quit_game):
        self.screen = screen
        self.transition_call = transition_call
        self.quit = quit_game
        self.images = {}
        self.is_loaded = False
        
        # Configurações de fonte
        self.fonte_pequena = pygame.font.SysFont("Arial", 20)
        self.fonte_media = pygame.font.SysFont("Arial", 24)
        self.fonte_titulo = pygame.font.SysFont("Arial", 36, bold=True)
        self.fonte_colegio = pygame.font.SysFont("Arial", 28, italic=True)
        
        # Elementos da interface
        self.botao_entrar = Botao(
            (Constantes.largura//2 - 100, 300), 
            (200, 50), 
            pygame.Color("dodgerblue"), 
            "Entrar", 
            self.fonte_media
        )
        
        # Campos de entrada
        self.campos = {
            "usuario": {
                "retangulo": pygame.Rect(Constantes.largura//2 - 150, 200, 300, 40),
                "texto": "",
                "ativo": False,
                "rotulo": "Usuário:",
                "senha": False
            },
            "senha": {
                "retangulo": pygame.Rect(Constantes.largura//2 - 150, 250, 300, 40),
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
    
    def load(self):
        self.images = {
            "background": pygame.image.load("imagens/tela_login.jpeg").convert(),  
        }

        self.is_loaded = all(image is not None for image in self.images.values())
    
    def run(self):
        if self.is_loaded:

            self.screen.fill(self.cor_fundo)
            self.screen.blit(self.images["background"])
        
            # Renderiza título e subtítulo
            self.renderizar_titulo()
        
            # Desenha campos de entrada
            for campo in self.campos.values():
             self.desenhar_campo(campo)
        
            # Desenha botão e mensagens
            self.botao_entrar.draw(self.screen)
            self.mostrar_mensagem_erro()
        
            # Processa eventos
            self.tratar_eventos()
        
            # Verifica ação do botão
            if self.botao_entrar.check_button():
             self.verificar_login()
    
    def renderizar_titulo(self):
        titulo = self.fonte_titulo.render("Policáro", True, self.cor_titulo)
        subtitulo = self.fonte_colegio.render("Colégio", True, self.cor_titulo)
        
        self.screen.blit(titulo, (Constantes.largura//2 - titulo.get_width()//2, 80))
        self.screen.blit(subtitulo, (Constantes.largura//2 - subtitulo.get_width()//2, 130))
    
    def desenhar_campo(self, campo):
        # Fundo do campo
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
            self.screen.blit(erro, (Constantes.largura//2 - erro.get_width()//2, 360))
    
    def tratar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            
            # Clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.processar_clique(event.pos)
            
            # Teclado
            if event.type == pygame.KEYDOWN:
                self.processar_tecla(event)
    
    def processar_clique(self, pos):
        # Ativa/desativa campos
        for nome, campo in self.campos.items():
            campo["ativo"] = campo["retangulo"].collidepoint(pos)
        
        # Limpa mensagem de erro ao interagir
        self.mensagem_erro = ""
    
    def processar_tecla(self, event):
        for campo in self.campos.values():
            if campo["ativo"]:
                if event.key == pygame.K_BACKSPACE:
                    campo["texto"] = campo["texto"][:-1]
                elif event.key == pygame.K_RETURN:
                    self.verificar_login()
                else:
                    campo["texto"] += event.unicode
    
    def verificar_login(self):
        usuario = self.campos["usuario"]["texto"]
        senha = self.campos["senha"]["texto"]
        
        if not usuario or not senha:
            self.mensagem_erro = "Preencha todos os campos!"
            return
        
        # Exemplo de validação - substitua pela sua lógica
        if usuario == "admin" and senha == "1234":
            print("Login bem-sucedido!")
            self.transition_call(TelaAdmin(self.screen, self.transition_call))
        else:
            self.mensagem_erro = "Credenciais inválidas!"
            print(f"Tentativa de login falhou: Usuário={usuario}")
