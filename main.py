import sys

import pygame

from SETTINGS import *


class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.game()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def game(self):
        while True:
            self.check_events()
            self.draw()
            self.refresh_screen()

    def draw(self):
        pass

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()