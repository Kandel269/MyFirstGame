import os
import sys

import pygame

from SETTINGS import *
from map import *

class Game():
    def __init__(self):
        pygame.init()

        self.load_textures()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1

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

    def game(self):
        self.map = Map()

        while True:
            self.check_events()
            self.refresh_screen()
            self.draw()

    def draw(self):
        for row in range(8):
            for col in range(8):
                square = row * MAP_SIZE + col
                self.draw_screen.blit(self.textures["enemy1"],self.map)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()