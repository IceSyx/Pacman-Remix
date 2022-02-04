import pygame
import os
from random import randint
from time import perf_counter
from sys import exit
from player import Player
from dot import Dot
from buff import Buff
from enemy import YellowEnemy, PinkEnemy, RedEnemy, BlueEnemy


pygame.font.init()


fontPath = os.path.join("font", "emulogic.ttf")


class Game:
    def __init__(self):
        self.running = True
        self.WIDTH = self.HEIGHT = 800
        self.FPS = 60
        self.score = 0
        self.bestScore = 0
        self.deathCount = self.FPS * 4
        self.dots = []
        self.buffs = []
        self.level = 1
        self.beginTimer = perf_counter()
        self.newBegin = 0
        self.timer = 0
        self.godMode = False
        self.buffCount = self.FPS * 4
        self.scoreCount = self.FPS * 0.5
        self.scoreList = []
        self.yellow = YellowEnemy(randint(0, 200), 200)
        self.pink = PinkEnemy(randint(200, 400), 200)
        self.blue = BlueEnemy(randint(400, 600), 200)
        self.red = RedEnemy(randint(600, 750), 200)
        self.ennemies = [self.yellow, self.pink, self.blue, self.red]
        self.mainFont = pygame.font.Font(fontPath, 23)
        self.displayFont = pygame.font.Font(fontPath, 15)
        self.lostFont = pygame.font.Font(fontPath, 15)
        self.pointsFont = pygame.font.Font(fontPath, 20)
        self.slainFont = self.pointsFont.render("+10", True, (255, 255, 255))
        self.dotFont = self.pointsFont.render("+1", True, (255, 255, 255))
        self.buffFont = self.pointsFont.render("+5", True, (255, 255, 255))
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pacman")
        self.player = Player(self.WIDTH / 2 - 25, self.HEIGHT - self.HEIGHT // 3)
        self.clock = pygame.time.Clock()

    def collide(self, obj1: object, obj2: object):
        offsetX = obj2.x - obj1.x
        offsetY = obj2.y - obj1.y
        return obj2.mask.overlap(obj2.mask, (offsetX, offsetY))

    def generate(self):
        #! Dots
        for i in range(5 * self.level):
            dot = Dot(randint(0, self.WIDTH - 20), randint(0, self.HEIGHT - 20))
            self.dots.append(dot)

        #! Buffs
        for i in range(2 if self.level > 10 else 1):
            buff = Buff(randint(0, self.WIDTH - 40), randint(0, self.HEIGHT - 40))
            self.buffs.append(buff)

    def redrawWindow(self, window: pygame.Surface):
        window.fill((0, 0, 0))  # TODO: retirer quand background

        #! Dots
        for dot in self.dots[:]:
            dot.draw(self.window)

        #! Buffs
        for buff in self.buffs[:]:
            buff.draw(self.window)

        #! Ennemies
        for enemy in self.ennemies[:]:
            enemy.draw(self.window)

        #! Player
        window.blit(self.player.currentImg, (self.player.x, self.player.y))

        #! Fonts
        startFont = self.mainFont.render(
            "Press any direction key to start!", True, (255, 255, 255)
        )
        scoreFont = self.displayFont.render(
            f"Score: {self.score}", True, (255, 255, 255)
        )
        timerFont = self.displayFont.render(
            f"Timer: {format(self.timer, '.1f')}", True, (255, 255, 255)
        )
        levelFont = self.displayFont.render(
            f"Level: {self.level}", True, (255, 255, 255)
        )
        deathFont = self.lostFont.render("You Lost !", True, (255, 255, 255))
        bestScoreFont = self.lostFont.render(
            f"Best Score: {'-' if self.bestScore == 0 else self.bestScore}",
            True,
            (255, 255, 255),
        )
        respawnFont = self.lostFont.render(
            f"Try again in {self.deathCount // 60} seconds", True, (255, 255, 255)
        )
        buffTime = self.displayFont.render(
            f"Buff Time left: {self.buffCount // 60}", True, (255, 255, 255)
        )
        if not self.player.started:
            window.blit(
                startFont,
                (
                    self.WIDTH / 2 - startFont.get_width() // 2,
                    self.HEIGHT / 3 + startFont.get_height(),
                ),
            )

        if self.player.started and not self.player.dead:
            window.blit(scoreFont, (10, 10))
            window.blit(timerFont, (self.WIDTH - timerFont.get_width() - 10, 10))
            window.blit(levelFont, (10, 10 + scoreFont.get_height()))

        if self.player.dead:
            window.blit(
                deathFont,
                (
                    self.WIDTH / 2 - deathFont.get_width() // 2,
                    self.HEIGHT / 3 + deathFont.get_height(),
                ),
            )
            window.blit(
                respawnFont,
                (
                    self.WIDTH / 2 - respawnFont.get_width() // 2,
                    self.HEIGHT / 3 + respawnFont.get_height() + 30,
                ),
            )
            window.blit(
                levelFont,
                (self.WIDTH / 2 - levelFont.get_width() // 2, self.HEIGHT / 2 + 10),
            )
            window.blit(
                bestScoreFont,
                (self.WIDTH / 2 - bestScoreFont.get_width() // 2, self.HEIGHT / 2 + 40),
            )
            window.blit(
                scoreFont,
                (self.WIDTH / 2 - scoreFont.get_width() // 2, self.HEIGHT / 2 + 70),
            )

        if self.player.buffed:
            window.blit(buffTime, (self.WIDTH / 2 - buffTime.get_width() // 2, 10))

        pygame.display.update()

    def handle_player_buff(self):
        pass

    def reset_game(self):
        #! Game Variables
        self.deathCount = self.FPS * 4
        self.buffCount = self.FPS * 4
        self.score = 0
        self.level = 1

        #! Player
        self.player.started = False
        self.player.buffed = False
        self.player.open = True
        self.player.dead = False
        self.player.x = self.WIDTH / 2 - 25
        self.player.y = self.HEIGHT - self.HEIGHT // 3
        self.player.X = self.player.Y = True

        #! Ennemies
        self.ennemies = [
            YellowEnemy(randint(0, 200), 200),
            PinkEnemy(randint(200, 400), 200),
            BlueEnemy(randint(400, 600), 200),
            RedEnemy(randint(600, 750), 200),
        ]

        #! Dots
        self.dots = []

        #! Buffs
        self.buffs = []

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.redrawWindow(self.window)

            #! Timer
            self.timer = perf_counter() - self.beginTimer

            #! If the player is dead
            if self.player.dead:
                self.deathCount -= 1
                if self.deathCount == 0:
                    self.reset_game()

            else:
                #! Make the player move
                self.player.move(self.WIDTH, self.HEIGHT)
                self.player.handle_direction()
                self.player.animate()

                #! Make the ennemies move towards player
                for enemy in self.ennemies[:]:
                    enemy.move(
                        self.player.x,
                        self.player.y,
                        self.player.started,
                        self.player.buffed,
                        self.WIDTH,
                        self.HEIGHT,
                    )

                    #! Check for collisions with ennemies
                    if (
                        self.collide(enemy, self.player)
                        and not self.godMode
                        and not self.player.buffed
                    ):
                        self.player.dead = True
                        if self.score > self.bestScore:
                            self.bestScore = self.score

                    #! If the payer ate a buff and collided with an enemy
                    elif self.collide(enemy, self.player) and self.player.buffed:
                        self.ennemies.remove(enemy)
                        self.score += 10
                        self.scoreList.append(
                            (
                                self.scoreCount,
                                self.slainFont,
                                enemy.x + 10,
                                enemy.y + 10,
                            )
                        )
                        # self.window.blit(self.slainFont, (enemy.x + 10, enemy.y + 10))
                        # pygame.display.update()

                #! Check for collisions with dots
                for dot in self.dots[:]:
                    if self.collide(dot, self.player):
                        self.dots.remove(dot)
                        self.score += 1
                        self.scoreList.append(
                            (self.scoreCount, self.dotFont, dot.x + 10, dot.y + 10)
                        )
                        # self.window.blit(self.dotFont, (dot.x + 10, dot.y + 10))
                        # pygame.display.update()

                #! Check the collisions with buffs
                for buff in self.buffs[:]:
                    if self.collide(buff, self.player):
                        self.buffs.remove(buff)
                        self.score += 5
                        self.scoreList.append(
                            (self.scoreCount, self.buffFont, buff.x + 30, buff.y + 30)
                        )
                        # self.window.blit(self.buffFont, (buff.x + 30, buff.y + 30))
                        # pygame.display.update()
                        self.player.buffed = True
                        self.handle_player_buff()

                #! Check if there is still Dot and Buff on the map
                if len(self.dots) == 0 and len(self.buffs) == 0 and self.player.started:
                    #! Dots
                    self.level += 1
                    for i in range(5 * self.level):
                        dot = Dot(
                            randint(0, self.WIDTH - 20),
                            randint(0, self.HEIGHT - 20),
                        )
                        self.dots.append(dot)

                    #! Buffs
                    for i in range(2 if self.level > 10 else 1):
                        buff = Buff(
                            randint(0, self.WIDTH - 40), randint(0, self.HEIGHT - 40)
                        )
                        self.buffs.append(buff)

                    #! Ennemies
                    if len(self.ennemies) == 1:
                        enemy = self.ennemies[0]
                        enemy.vel = self.player.vel - 1

                #! Display the Scores during 0.5s
                newScoreList = []
                for item in self.scoreList[:]:
                    timer, score, x, y = item
                    if timer > 0:
                        newScoreList.append((timer - 1, score, x, y))
                        self.window.blit(score, (x, y))
                        pygame.display.update()
                self.scoreList = newScoreList

            #! Check if there is still ennemies
            if len(self.ennemies) == 0:
                self.score += 20
                self.player.buffed = False
                self.ennemies = [
                    YellowEnemy(randint(0, 200), 200),
                    PinkEnemy(randint(200, 400), 200),
                    BlueEnemy(randint(400, 600), 200),
                    RedEnemy(randint(600, 750), 200),
                ]

            #! Check if the player is buffed
            if self.player.buffed:
                self.buffCount -= 1
                for enemy in self.ennemies[:]:
                    enemy.img = enemy.vulnerableImgs[0]
                if self.buffCount == self.FPS:
                    self.player.buffed = False
            else:
                self.buffCount = self.FPS * 4
                for enemy in self.ennemies[:]:
                    enemy.img = enemy.srcImg

            #! Check the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    #! UP
                    if (
                        event.key == pygame.K_z or event.key == pygame.K_UP
                    ) and self.player.Y:
                        if not self.player.started:
                            self.generate()
                            self.beginTimer = perf_counter()
                        self.player.Y, self.player.X = False, True
                        self.player.direction = "up"
                        self.player.started = True

                    #! RIGHT
                    elif (
                        event.key == pygame.K_d or event.key == pygame.K_RIGHT
                    ) and self.player.X:
                        if not self.player.started:
                            self.generate()
                            self.beginTimer = perf_counter()
                        self.player.Y, self.player.X = True, False
                        self.player.direction = "right"
                        self.player.started = True

                    #! DOWN
                    elif (
                        event.key == pygame.K_s or event.key == pygame.K_DOWN
                    ) and self.player.Y:
                        if not self.player.started:
                            self.generate()
                            self.beginTimer = perf_counter()
                        self.player.Y, self.player.X = False, True
                        self.player.direction = "down"
                        self.player.started = True

                    #! LEFT
                    elif (
                        event.key == pygame.K_q or event.key == pygame.K_LEFT
                    ) and self.player.X:
                        if not self.player.started:
                            self.generate()
                            self.beginTimer = perf_counter()
                        self.player.Y, self.player.X = True, False
                        self.player.direction = "left"
                        self.player.started = True

                    #! Enable / Disable GodMode
                    elif event.key == pygame.K_g:
                        self.godMode = not self.godMode


game = Game()
game.run()
