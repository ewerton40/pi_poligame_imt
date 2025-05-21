import pygame
from interfaces.database import Database

WINDOW_SIZE = (1280, 720)
TILE_SIZE = 30
PLAYER_VELOCITY = 200
DATABASE = Database()

class User:
    def __init__(self, id):
        self.player_id = id

    def get_id(self) -> int:
        return self.player_id

    def set_id(self, id):
        self.player_id = id

def break_line(text:str, start_pos: pygame.Vector2, max_size=300) -> list[Typography]:
    texts = []
    chars = []
    total_w = 0
    indice = 0
    chars = text.split(" ")
    for i in chars:
        t = pygame.font.SysFont("Arial", 32).render(i, True, "black")
        indice = chars.index(i)
        if total_w + t.get_width() > max_size:
            start_pos.y += 20
            total_w = 0
            texts.append(Typography(((start_pos.x, start_pos.y)),
                                    ' '.join(chars[:indice + 1]), "white"))
            chars = chars[indice + 1:]
        elif total_w < max_size and indice == len(chars) - 1:
                start_pos.y += 20
                texts.append(Typography(((start_pos.x, start_pos.y)),
                                        ' '.join(chars[:indice + 1]), "white"))

        total_w += t.get_width()

        return texts

USER = User(None)