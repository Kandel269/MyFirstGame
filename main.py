import os
import sys
import pygame

from SETTINGS import *
from tile import *
from player import *

class Game():
    def __init__(self):
        pygame.init()

        self.load_textures()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.player = Player()
        self.tiles = []

        self.collision_types = {}

        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img\\" + img)
            self.textures[img.replace(".png","")] = texture

    def colision_test_player(self):
        hit_list = []
        for tile in self.tiles:
            if self.player.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_player(self):
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.player.x += self.player.x_speed
        hit_list = self.colision_test_player()
        for tile in hit_list:
            if self.player.x_speed > 0:
                self.player.right = tile.left
                self.collision_types['right'] = True
            elif self.player.x_speed < 0:
                self.player.left = tile.right
                self.collision_types['left'] = True

        if self.player.during_jump:
            if self.player.air_timer <= MAX_JUMP:
                self.player.y += self.player.y_speed - JUMP_SPEED
            else:
                self.player.y += self.player.y_speed
        else:
            self.player.y += self.player.y_speed

        hit_list = self.colision_test_player()
        for tile in hit_list:
            if self.player.y_speed > 0:
                self.player.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player.y_speed < 0:
                self.player.top = tile.bottom
                self.collision_types['top'] = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

        self.move_player()
        if self.collision_types['bottom']:
            self.player.air_timer = 0
            self.player.during_jump = False
        else:
            self.player.air_timer += 1

        self.player.reset_speed()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.x_speed += int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_LEFT]:
            self.player.x_speed -= int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_SPACE] and self.player.air_timer < 5 and not self.player.during_jump:
            self.player.y_speed -= JUMP_SPEED
            self.player.during_jump = True

    def game(self):

        for x in range(16):
            self.tiles.append(Tile((x * 30), 290, "enemy1"))
        for y in range(10):
            self.tiles.append(Tile(0, y * 32, "enemy1"))
            self.tiles.append(Tile(450, y * 32, "enemy1"))

        while True:
            self.check_keys()
            self.check_events()
            self.refresh_screen()
            self.draw()

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,0))
        self.draw_screen.blit(self.textures["player"],self.player)
        for tile in self.tiles:
            self.draw_screen.blit(self.textures[tile.tile_name], tile)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()