import os
import random
import sys
import pygame

from SETTINGS import *
from tile import *
from player import *
from enemy import *
from bonus import *

class Game():
    def __init__(self):
        pygame.init()

        self.load_textures()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1

        self.player = Player()
        self.points = 0
        self.tiles = []
        self.hearts_list = []

        self.font_points = pygame.font.Font(r"Pacifico.ttf",40)

        self.collision_types = {}

        self.enemies_list = []
        self.bonus_list = []

        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img\\" + img)
            self.textures[img.replace(".png","")] = texture

    def colision_test_player(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.player.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_player(self):
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.player.x += self.player.x_speed
        hit_list = self.colision_test_player(self.tiles)
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

        hit_list = self.colision_test_player(self.tiles)
        for tile in hit_list:
            if self.player.y_speed > 0:
                self.player.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player.y_speed < 0:
                self.player.top = tile.bottom
                self.collision_types['top'] = True

    def create_enemy(self):
        if random.randint(1,CREATE_ENEMY_RATIO) == 1:
            x = random.randint(30,430)
            self.enemies_list.append(Bomb(x, -100, "enemy2"))

    def enemy_collision(self):
        for enemy in self.colision_test_player(self.enemies_list):
            self.enemies_list.remove(enemy)
            self.player.hp -= 1

    def bonus_collision(self):
        for bonus in self.colision_test_player(self.bonus_list):
            self.points += bonus.points
            self.bonus_list.remove(bonus)

    def create_bonus(self):
        if random.randint(1, CREATE_BONUS_RATIO) == 1:
            x = random.randint(30,430)
            self.bonus_list.append(Bonus(x, -100, "enemy3", 100))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies_list:
                    enemy.move()
            if event.type == self.BONUSMOVE:
                for bonus in self.bonus_list:
                    bonus.move()

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

    def check_hearts(self):
        self.hearts_list = []
        for heart in range(self.player.hp):
            self.hearts_list.append(Tile(heart * 30, 0, "heart_full"))
        for heart in range(3 - self.player.hp):
            self.hearts_list.append(Tile((heart + self.player.hp) * 30, 0 , "heart_empty"))

    def check_points(self):
        text = str(self.points)
        self.surf_points = self.font_points.render(text, False,(255,0,0))
        self.points_txt = self.surf_points.get_rect(center=(int(DRAW_SCREEN_SIZE[0]/2),10))

    def game(self):
        self.ENEMYMOVE = pygame.USEREVENT
        pygame.time.set_timer(self.ENEMYMOVE, ENEMY_MOVE_RATIO)
        self.BONUSMOVE = pygame.USEREVENT
        pygame.time.set_timer(self.BONUSMOVE, ENEMY_MOVE_RATIO)

        for x in range(16):
            self.tiles.append(Tile((x * 30), 290, "enemy1"))
        for y in range(10):
            self.tiles.append(Tile(0, y * 32, "enemy1"))
            self.tiles.append(Tile(450, y * 32, "enemy1"))

        while True:
            self.check_keys()
            self.check_events()

            # player
            self.move_player()
            if self.collision_types['bottom']:
                self.player.air_timer = 0
                self.player.during_jump = False
            else:
                self.player.air_timer += 1
            self.player.reset_speed()

            self.check_hearts()

            # enemy
            self.enemy_collision()
            self.create_enemy()

            for enemy in self.enemies_list:
                if enemy.y > DRAW_SCREEN_SIZE[1]:
                    self.enemies_list.remove(enemy)

            # bonus
            self.bonus_collision()
            self.create_bonus()

            #points
            self.check_points()

            self.refresh_screen()
            self.draw()

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,0))
        self.draw_screen.blit(self.textures["player"],self.player)
        for tile in self.tiles:
            self.draw_screen.blit(self.textures[tile.tile_name], tile)
        for enemy in self.enemies_list:
            self.draw_screen.blit(self.textures[enemy.enemy_name], enemy)
        for bonus in self.bonus_list:
            self.draw_screen.blit(self.textures[bonus.bonus_name], bonus)
        for heart in self.hearts_list:
            self.draw_screen.blit(self.textures[heart.tile_name], heart)
        self.draw_screen.blit(self.surf_points,self.points_txt)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()