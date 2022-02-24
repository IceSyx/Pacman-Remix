import pygame
import os


WHITE = (255, 255, 255)


class Dot:
    def __init__(
        self,
        x: int,
        y: int,
    ):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "dot.png")), (20, 20)
        )
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window: pygame.Surface):
        window.blit(self.img, (self.x, self.y))
