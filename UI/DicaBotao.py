import pygame

class DicaBotao:
    def __init__(self, position:tuple[int,int],
                  default_image:pygame.Surface, hover_image:pygame.Surface):
        self.position = position
        self.default_image = default_image
        self.hover_image = hover_image
        self.image = self.default_image
        self.rect = self.image.get_rect(topleft=self.position)
        self.clicked = False
        self.activated = False
        self.state = False

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def check_click(self):
        if self.activated:
            return  # Já foi clicado, não faz mais nada

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed and not self.clicked:
                self.clicked = True  # Marca como pressionado
            elif not mouse_pressed and self.clicked:
                self.clicked = False  # Solta o clique
                self.activated = True  # Marca como ativado permanentemente
                self.image = self.hover_image  # Troca a imagem apenas uma vez
        else:
            if not mouse_pressed:
                self.clicked = False  # Garante reset do clique fora do botão