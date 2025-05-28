# Classes/item_lista.py
import pygame

class ItemLista:
    def __init__(self, pergunta_data, y_pos, largura_tela, on_excluir=None):
        self.pergunta_data = pergunta_data
        self.y_pos = y_pos
        self.largura_tela = largura_tela
        self.on_excluir = on_excluir

        # Configurações de layout
        self.margem_x = 10
        self.margem_y_texto = 10
        self.largura_item = largura_tela - (2 * self.margem_x)  # Corrigido nome da variável (largem_item -> largura_item)
        self.altura_item = 70

        self.rect = pygame.Rect(self.margem_x, self.y_pos, self.largura_item, self.altura_item)
        
        # Fontes
        self.fonte_enunciado = pygame.font.Font(None, 24)
        self.fonte_detalhes = pygame.font.Font(None, 20)
        self.font_botao = pygame.font.Font(None, 20)

        # Configurações do botão
        self.largura_botao = 80
        self.altura_botao = 30
        self.btn_excluir_rel_x = self.largura_item - self.largura_botao - self.margem_x
        self.btn_excluir_rel_y = self.margem_y_texto + 5

    def desenhar(self, surface, scroll_offset=0):
        """Desenha o item na superfície com o offset de scroll aplicado"""
        draw_rect = self.rect.copy()
        draw_rect.y = self.y_pos + scroll_offset

        # Desenha o fundo e borda do item
        pygame.draw.rect(surface, (150, 150, 150), draw_rect, border_radius=5)
        pygame.draw.rect(surface, (100, 100, 100), draw_rect, 2, border_radius=5)

        # Renderiza o enunciado com quebra de linha
        enunciado = self.pergunta_data["enunciado"]
        max_enunciado_width = self.largura_item - (2 * self.margem_x) - self.largura_botao - self.margem_x
        enunciado_lines = self._wrap_text(enunciado, self.fonte_enunciado, max_enunciado_width)
        
        text_y_offset = draw_rect.y + self.margem_y_texto
        for line in enunciado_lines:
            line_surf = self.fonte_enunciado.render(line, True, (0, 0, 0))
            surface.blit(line_surf, (draw_rect.x + self.margem_x, text_y_offset))
            text_y_offset += line_surf.get_height()

        # Renderiza os detalhes (dificuldade e matéria)
        detalhes_texto = self._formatar_detalhes()
        detalhes_surf = self.fonte_detalhes.render(detalhes_texto, True, (0, 0, 0))
        surface.blit(detalhes_surf, (draw_rect.x + self.margem_x, text_y_offset + 5))

        # Desenha o botão de exclusão
        self._desenhar_botao_excluir(surface, draw_rect)

    def _formatar_detalhes(self):
        """Formata os detalhes da pergunta para exibição"""
        materia = self.pergunta_data.get('nome_materia', self.pergunta_data['materia_id'])
        return f"Dificuldade: {self.pergunta_data['dificuldade']} | Matéria: {materia}"

    def _desenhar_botao_excluir(self, surface, draw_rect):
        """Desenha o botão de exclusão"""
        btn_x = draw_rect.x + self.btn_excluir_rel_x
        btn_y = draw_rect.y + self.btn_excluir_rel_y
        
        btn_rect = pygame.Rect(btn_x, btn_y, self.largura_botao, self.altura_botao)
        pygame.draw.rect(surface, (200, 0, 0), btn_rect, border_radius=3)
        
        texto_surf = self.font_botao.render("EXCLUIR", True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(center=btn_rect.center)
        surface.blit(texto_surf, texto_rect)

    def verificar_clique_botoes(self, mouse_pos_relative_to_list_surface, scroll_offset=0):
        """Verifica se o botão de exclusão foi clicado"""
        item_draw_y_pos = self.y_pos + scroll_offset

        actual_rect_excluir = pygame.Rect(
            self.rect.x + self.btn_excluir_rel_x,
            item_draw_y_pos + self.btn_excluir_rel_y,
            self.largura_botao,
            self.altura_botao
        )

        if actual_rect_excluir.collidepoint(mouse_pos_relative_to_list_surface):
            if self.on_excluir:
                self.on_excluir(self.pergunta_data["id"])
            return True
        return False
    
    def _wrap_text(self, text, font, max_width):
        """Quebra o texto em múltiplas linhas se necessário"""
        if not text:
            return [""]

        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]