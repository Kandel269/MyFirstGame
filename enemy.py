import pygame

from SETTINGS import *

class Enemy(pygame.Rect):
    def __init__(self, x, y, enemy_name, enemy_speed, player_collision = True):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.enemy_name = enemy_name
        self.enemy_speed = enemy_speed
        self.player_collision = player_collision

    def move(self):
        self.x += 0
        self.y += ENEMY_SPEED + self.enemy_speed

class Bomb(Enemy):
    def __init__(self, x, y, enemy_name, enemy_speed, player_collision = False):
        super().__init__(x, y, enemy_name, enemy_speed, player_collision)
