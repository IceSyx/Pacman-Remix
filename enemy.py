import pygame
import math
import os


class Enemy:
    def __init__(self):
        self.x = None
        self.y = None
        self.img = None
        self.animationCount = 0
        self.vulnerable = False
        self.vel = 2
        self.vulnerableImgs = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "vulnerable1.png")), (50, 50)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "vulnerable2.png")), (50, 50)
            ),
        ]

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.img.get_width()

    def handle_image(self, buffed, buffTime, FPS):
        if buffed:
            self.animationCount = buffTime
            if self.animationCount % (FPS / 2) == 0:
                self.img = self.vulnerableImgs[0]
            elif self.animationCount % (FPS / 4) == 0:
                self.img = self.vulnerableImgs[1]

    def move(
        self,
        playerX: int,
        playerY: int,
        started: bool,
        buffed: bool,
        width: int,
        height: int,
    ):
        hypotenuse = math.sqrt((self.x - playerX) ** 2 + (self.y - playerY) ** 2)
        vector = (playerX - self.x, playerY - self.y)
        goalX = vector[0] / hypotenuse
        goalY = vector[1] / hypotenuse

        #! Move towards the player
        if started and not buffed:
            self.x += goalX * self.vel
            self.y += goalY * self.vel

        #! Move away from the player
        elif started and buffed:
            if self.x + self.get_width() < width and self.x > 0:
                self.x -= goalX * self.vel
            if self.y + self.get_height() < height and self.y > 0:
                self.y -= goalY * self.vel


class RedEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.srcImg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "red.png")), (50, 50)
        )
        self.img = self.srcImg
        self.x = x
        self.y = y
        self.vel = 2
        self.mask = pygame.mask.from_surface(self.img)


class BlueEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.srcImg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "blue.png")), (50, 50)
        )
        self.img = self.srcImg
        self.x = x
        self.y = y
        self.vel = 5
        self.mask = pygame.mask.from_surface(self.img)


class YellowEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.srcImg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "yellow.png")), (50, 50)
        )
        self.img = self.srcImg
        self.x = x
        self.y = y
        self.vel = 3
        self.mask = pygame.mask.from_surface(self.img)


class PinkEnemy(Enemy):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.srcImg = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "pink.png")), (50, 50)
        )
        self.x = x
        self.img = self.srcImg
        self.y = y
        self.vel = 4
        self.mask = pygame.mask.from_surface(self.img)
