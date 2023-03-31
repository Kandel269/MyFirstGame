import pygame
from SETTINGS import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        # self.y = 260
        self.y = 100
        self.h = 20
        self.w = 20
        self.y_speed = GRAVITY
        self.x_speed = 0
        self.hp = PLAYER_HP
        self.max_jump_y = MAX_JUMP
        self.air_timer = 0
        self.during_jump = False

    def reset_speed(self):
        self.x_speed = 0
        self.y_speed = GRAVITY
