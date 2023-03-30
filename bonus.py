import pygame

from SETTINGS import *

class Bonus(pygame.Rect):
    def __init__(self,x,y,bonus_name, points):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.bonus_name = bonus_name
        self.points = points

    def move(self):
        self.x += 0
        self.y += BONUS_SPEED