import pygame
import os

imagesIndex = {"up": 0, "right": 1, "down": 2, "left": 3, None: 1}


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.X = self.Y = True
        self.vel = 7
        self.direction = None
        self.open = True
        self.dead = False
        self.buffed = False
        self.started = False
        self.animationCount = 0
        self.openImgs = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "open", "up.png")), (50, 50)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "open", "right.png")), (50, 50)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "open", "down.png")), (50, 50)
            ),
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "open", "left.png")), (50, 50)
            ),
        ]
        self.closedImgs = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "closed.png")), (50, 50)
            ),
        ]
        self.imgs = [self.openImgs, self.closedImgs]
        self.currentImg = self.imgs[0][0]
        self.mask = pygame.mask.from_surface(self.currentImg)

    def animate(self):
        if self.started:
            self.animationCount += 1
            if self.animationCount % 8 == 0:
                self.open = not self.open

    def get_width(self):
        return self.currentImg.get_width()

    def get_height(self):
        return self.currentImg.get_height()

    def move(self, width: int, height: int):
        if self.direction != None and self.started:
            if self.direction == "left" and 0 < self.x:
                self.x -= self.vel
            elif self.direction == "right" and width > self.x + self.get_width():
                self.x += self.vel
            elif self.direction == "up" and 0 < self.y:
                self.y -= self.vel
            elif self.direction == "down" and height > self.y + self.get_height() + 15:
                self.y += self.vel

    def handle_direction(self):
        if self.open:
            self.currentImg = self.imgs[0][imagesIndex[self.direction]]
        else:
            self.currentImg = self.imgs[1][0]
