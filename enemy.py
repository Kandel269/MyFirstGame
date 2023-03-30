import pygame

from SETTINGS import *

class Bomb(pygame.Rect):
    def __init__(self,x,y,bomb_name):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.bomb_name = bomb_name

    def move(self):
        self.x += 0
        self.y += ENEMY_SPEED