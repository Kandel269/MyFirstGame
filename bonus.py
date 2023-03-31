import pygame

from SETTINGS import *

class Bonus(pygame.Rect):
    def __init__(self,x,y,bonus_name, bonus_speed, points):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.bonus_name = bonus_name
        self.points = points
        self.bonus_speed = bonus_speed

    def move(self):
        self.x += 0
        self.y += BONUS_SPEED + self.bonus_speed