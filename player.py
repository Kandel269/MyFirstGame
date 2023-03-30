import pygame
from SETTINGS import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        # self.y = 260
        self.y = 100
        self.h = 20
        self.y_speed = GRAVITY
        self.x_speed = 0
        self.w = 20
        self.hp = 3

        self.max_jump_y = MAX_JUMP
        self.during_jump = False

    def jump(self, direction):
        if direction == "up":
            self.y -= JUMP_SPEED
        else:
            self.y += JUMP_SPEED

    def move(self):
        self.y = self.y + self.y_speed
        self.x = self.x + self.x_speed

    def reset_speed(self):
        self.x_speed = 0
        self.y_speed = GRAVITY
