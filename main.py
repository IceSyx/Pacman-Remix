import pygame
from random import randint
from time import perf_counter
from sys import exit
from player import Player
from dot import Dot
from buff import Buff
from enemy import YellowEnemy, PinkEnemy, RedEnemy, BlueEnemy


pygame.font.init()


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
        self.timer = 0
        self.godMode = False
        self.buffCount = self.FPS * 8
        self.yellow = YellowEnemy(randint(0, 200), 200)
        self.pink = PinkEnemy(randint(200, 400), 200)
        self.blue = BlueEnemy(randint(400, 600), 200)
        self.red = RedEnemy(randint(600, 750), 200)
        self.ennemies = [self.yellow, self.pink, self.blue, self.red]
        self.mainFont = pygame.font.SysFont("sans serif", 70)
        self.displayFont = pygame.font.SysFont("sans serif", 40)
        self.lostFont = pygame.font.SysFont("sans serif", 40)
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
        for i in range(3 if self.level > 10 else 1):
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

        pygame.display.update()

    def handle_player_buff(self):
        pass

    def reset_game(self):
        #! Game Variables
        self.deathCount = self.FPS * 4
        self.score = 0
        self.level = 1

        #! Player
        self.player.started = False
        self.player.open = True
        self.player.dead = False
        self.player.x = self.WIDTH / 2 - 25
        self.player.y = self.HEIGHT - self.HEIGHT // 3
        self.player.X = self.player.Y = True

        #! Ennemies
        self.yellow.x, self.yellow.y = randint(0, 200), 200
        self.pink.x, self.pink.y = randint(200, 400), 200
        self.blue.x, self.blue.y = randint(400, 600), 200
        self.red.x, self.red.y = randint(600, 750), 200

        #! Dots
        self.dots = []

        #! Buffs
        self.buffs = []

    def run(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.redrawWindow(self.window)

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
                for enemy in self.ennemies:
                    enemy.move(self.player.x, self.player.y, self.player.started)

                    #! Check for collisions with ennemies
                    if (
                        self.collide(enemy, self.player)
                        and not self.godMode
                        and not self.player.buffed
                    ):
                        self.player.dead = True
                        if self.score > self.bestScore:
                            self.bestScore = self.score

                #! Check for collisions with dots
                for dot in self.dots[:]:
                    if self.collide(dot, self.player):
                        self.dots.remove(dot)
                        self.score += 1

                #! Check the collisions with buffs
                for buff in self.buffs[:]:
                    if self.collide(buff, self.player):
                        self.buffs.remove(buff)
                        self.score += 5
                        # self.player.buffed = True
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
                    for i in range(3 if self.level > 10 else 1):
                        buff = Buff(
                            randint(0, self.WIDTH - 40), randint(0, self.HEIGHT - 40)
                        )
                        self.buffs.append(buff)

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
                        self.player.Y, self.player.X = False, True
                        self.player.direction = "up"
                        self.player.started = True

                    #! RIGHT
                    elif (
                        event.key == pygame.K_d or event.key == pygame.K_RIGHT
                    ) and self.player.X:
                        if not self.player.started:
                            self.generate()
                        self.player.Y, self.player.X = True, False
                        self.player.direction = "right"
                        self.player.started = True

                    #! DOWN
                    elif (
                        event.key == pygame.K_s or event.key == pygame.K_DOWN
                    ) and self.player.Y:
                        if not self.player.started:
                            self.generate()
                        self.player.Y, self.player.X = False, True
                        self.player.direction = "down"
                        self.player.started = True

                    #! LEFT
                    elif (
                        event.key == pygame.K_q or event.key == pygame.K_LEFT
                    ) and self.player.X:
                        if not self.player.started:
                            self.generate()
                        self.player.Y, self.player.X = True, False
                        self.player.direction = "left"
                        self.player.started = True

                    #! Activate / Disable GodMode
                    elif event.key == pygame.K_g:
                        self.godMode = not self.godMode


game = Game()
game.run()
