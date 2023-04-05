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
        self.y += ENEMY_SPEED

class Bomb(Enemy):
    def __init__(self,x,y,enemy_name,enemy_speed = 1, player_collision = False):
        super().__init__(x,y,enemy_name,enemy_speed, player_collision)
        self.enemy_frame = 0
        self.enemy_name = enemy_name
        self.last_update = 0
        self.animation_cooldown = BOMB_ANIMATION_COOLDOWN
        self.on_ground = False
        self.detonation_time = 0

class Boom(pygame.Rect):
    def __init__(self,x,y,enemy_name, animation_cooldown):
        self.x = x
        self.y = y
        self.h = 100
        self.w = 100
        self.enemy_name = enemy_name
        self.animation_cooldown = animation_cooldown
        self.dmg = False