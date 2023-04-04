import pygame

from SETTINGS import *

class Enemy(pygame.Rect):
    def __init__(self,x,y,enemy_name):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.enemy_name = enemy_name

    def move(self):
        self.x += 0
        self.y += ENEMY_SPEED

class Bomb(Enemy):
    def __init__(self,x,y,enemy_name):
        super().__init__(x,y,enemy_name)


