import pygame
import math
import os


class Enemy:
    def __init__(self):
        self.x = None
        self.y = None
        self.img = None
        self.vel = 2

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.img.get_width()

    def move(self, playerX: int, playerY: int, started: bool):
        hypotenuse = math.sqrt((self.x - playerX) ** 2 + (self.y - playerY) ** 2)
        vector = (playerX - self.x, playerY - self.y)
        goalX = vector[0] / hypotenuse
        goalY = vector[1] / hypotenuse
        if started:
            self.x += goalX * self.vel
            self.y += goalY * self.vel


class RedEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "red.png")), (50, 50)
        )
        self.x = x
        self.y = y
        self.vel = 2
        self.mask = pygame.mask.from_surface(self.img)


class BlueEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "blue.png")), (50, 50)
        )
        self.x = x
        self.y = y
        self.vel = 5
        self.mask = pygame.mask.from_surface(self.img)


class YellowEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "yellow.png")), (50, 50)
        )
        self.x = x
        self.y = y
        self.vel = 3
        self.mask = pygame.mask.from_surface(self.img)


class PinkEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.img = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "pink.png")), (50, 50)
        )
        self.x = x
        self.y = y
        self.vel = 4
        self.mask = pygame.mask.from_surface(self.img)
