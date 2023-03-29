import pygame
from SETTINGS import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 260
        self.h = 20
        self.w = 20
        self.hp = 3

        self.max_jump_y = MAX_JUMP
        self.during_jump = False

    def jump(self, direction):
        if direction == "up":
            self.y -= JUMP_SPEED
        else:
            self.y += JUMP_SPEED