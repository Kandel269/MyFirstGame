import pygame
from SETTINGS import *


class Map(pygame.Rect):
    def __init__(self):
        self.x = int(DRAW_SCREEN_SIZE[0] / 2)
        self.y = 150
        self.h = 32
        self.w = 32
        self.map = (
            "#""#"


        )
