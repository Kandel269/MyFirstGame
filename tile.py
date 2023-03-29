import pygame
from SETTINGS import *


class Tile(pygame.Rect):
    def __init__(self,x,y,tile_name):
        self.x = x
        self.y = y
        self.h = 30
        self.w = 32
        self.tile_name = "enemy1"
