import pygame
from SETTINGS import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 260
        self.h = 20
        self.w = 20
        self.hp = 3
        self.during_jump = False

    def jump(self):
        self.y -= JUMP_SPEED

