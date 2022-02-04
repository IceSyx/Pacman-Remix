import pygame
import os


class Buff:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "buff.png")), (40, 40)
        )
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window: pygame.Surface):
        window.blit(self.img, (self.x, self.y))
