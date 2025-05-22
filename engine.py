import pygame
from Telas.Tela import Tela
from Telas.TelaInicio import TelaInicio
from Telas.TelaPergunta import TelaPergunta
from util import WINDOW_SIZE

class Engine():
    def __init__(self):
        # Initializes pygame modules
        pygame.init()

        self.screen = pygame.display.set_mode(WINDOW_SIZE,
                                               pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.display.set_caption("Poligame")
        icon = pygame.image.load("imagens/logo_poliedro.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True
        self.transition = 0
        self.active_scene: Tela | None = None
        self.previous_scene: Tela | None = None
        self.next_scene: Tela  = TelaInicio(self.screen, self.call_transition, self.quit)
        self.loaded = False

    def run(self):

        while self.running:
            if not self.loaded:
                self.transition += 1
                if self.transition > 60:
                    self.load_scene(self.next_scene)
                    self.loaded = True
                    self.transition = -60
            if self.transition < 0:
                self.transition += 1

            # Creates an event loop
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

            if self.active_scene:
                self.active_scene.run()

            if self.transition:
                transition_surf = pygame.Surface(WINDOW_SIZE)
                transition_surf.set_colorkey("green")
                pygame.draw.circle(transition_surf, "green",
                                   (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2),
                                    (60 - abs(self.transition)) * 10)
                self.screen.blit(transition_surf, (0, 0))

            pygame.display.update() # type: ignore

            # Limits the frame rate to 60 FPS
            self.clock.tick(60)

        pygame.quit()

    def load_scene(self, scene: Tela):
        self.previous_scene = self.active_scene
        scene.load()

        if scene.is_loaded:
            self.active_scene = scene

    def call_transition(self, scene: Tela):
        self.next_scene = scene
        self.loaded = False

    def go_back(self):
        if self.previous_scene:
            self.call_transition(self.previous_scene)

    def quit(self):
        self.running = False
