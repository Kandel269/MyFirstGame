import os
import sys
import pygame

from SETTINGS import *
from tile import *
from player import *

class Game():
    def __init__(self):
        pygame.init()

        self.load_textures()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.player = Player()
        self.tiles = []

        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img\\" + img)
            self.textures[img.replace(".png","")] = texture

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.x += int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_LEFT]:
            self.player.x -= int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_SPACE] and not self.player.during_jump:
            self.player.during_jump = True


    def game(self):

        for x in range(16):
            self.tiles.append(Tile((x * 30), 290, "enemy1"))
        for y in range(10):
            self.tiles.append(Tile(0, y * 32, "enemy1"))
            self.tiles.append(Tile(450, y * 32, "enemy1"))

        while True:

            if self.player.during_jump:
                self.player.jump()
            self.check_keys()
            self.check_events()
            self.refresh_screen()
            self.draw()

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,0))
        self.draw_screen.blit(self.textures["player"],self.player)
        for tile in self.tiles:
            self.draw_screen.blit(self.textures[tile.tile_name], tile)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()