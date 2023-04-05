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
        # self.load_sounds()

        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.current_time = pygame.time.get_ticks()

        self.player = Player()
        self.points = 0
        self.tiles_list = []
        self.hearts_list = []

        self.font_points = pygame.font.Font(r"Pacifico.ttf",40)
        self.font_end = pygame.font.Font(r"Pacifico.ttf",20)

        self.collision_types = {}

        self.enemies_list = []
        self.bonus_list = []
        self.boom_list = []

        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img\\" + img)
            texture.set_colorkey((255,255,255))
            self.textures[img.replace(".png","")] = texture

    # def load_sounds(self):
    #     self.sounds = {}
    #     for sound in os.listdir("sounds"):
    #         file = pygame.mixer.Sound("sounds\\" + sound)
    #         self.sounds[sound.replace(".wav", "")] = file


    def colision_test_player(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.player.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_player(self):
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        self.player.x += self.player.x_speed
        hit_list = self.colision_test_player(self.tiles_list)
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

        hit_list = self.colision_test_player(self.tiles_list)
        for tile in hit_list:
            if self.player.y_speed > 0:
                self.player.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.player.y_speed < 0:
                self.player.top = tile.bottom
                self.collision_types['top'] = True

    def colision_test_bomb(self, tiles,enemy):
        hit_list = []
        for tile in tiles:
            if enemy.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_bomb(self,enemy):

        enemy.move()
        hit_list = self.colision_test_bomb(self.tiles_list, enemy)

        if (enemy.on_ground == True) and self.current_time >= enemy.detonation_time:
            boom = Boom(int(enemy.topleft[0]) - 40, int(enemy.topleft[1]) - 40, "explosion",self.current_time + BOOM_ANIMATION_COOLDOWN)
            self.boom_list.append(boom)
            self.enemies_list.remove(enemy)

        for tile in hit_list:
            enemy.bottom = tile.top
            enemy.on_ground = True
            if enemy.detonation_time == 0:
                enemy.detonation_time = self.current_time + BOMB_DETONATION_TIME
                enemy.enemy_frame += 1

    def boom_life(self):
        for boom in self.boom_list:
            if self.current_time >= boom.animation_cooldown:
                self.boom_list.remove(boom)

    def create_enemy(self):
        x = random.randint(31, 430)
        if random.randint(1,CREATE_ENEMY_RATIO) == 1:
            self.enemies_list.append(Enemy(x, -100, "lightning", 0))
        if random.randint(1, CREATE_ENEMY_RATIO*7) == 1:
            self.enemies_list.append(Bomb(x, -100, "bomb", 2))

    def create_tile(self):
        x = random.randint(31, 430)
        y = random.randint(0, 290)
        if random.randint(1,1000) == 1:
            self.tiles_list.append(Tile(x,y,"wall",0))

    def enemy_collision(self):
        for enemy in self.colision_test_player(self.enemies_list):
            if enemy.player_collision:
                self.enemies_list.remove(enemy)
                self.player.hp -= 1
            #     self.sounds['lose_life'].play()

    def bonus_collision(self):
        for bonus in self.colision_test_player(self.bonus_list):
            self.points += bonus.points
            self.bonus_list.remove(bonus)
            # self.sounds['collect'].play()

    def boom_collision(self):
        for boom in self.colision_test_player(self.boom_list):
            if boom.dmg == False:
                self.player.hp -= 1
                boom.dmg = True

    def create_bonus(self):
        x = random.randint(30, 430)
        if random.randint(1, CREATE_BONUS_RATIO) == 1:
            self.bonus_list.append(Bonus(x, -100, "G1",0, 100))
        if random.randint(1, (CREATE_BONUS_RATIO*5)) == 1:
            self.bonus_list.append(Bonus(x, -100, "G2", 2, 300))
        if random.randint(1, (CREATE_BONUS_RATIO*20)) == 1:
            self.bonus_list.append(Bonus(x, -100, "G3", 2, 500))


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies_list:
                    if isinstance(enemy,Bomb):
                        self.move_bomb(enemy)
                    else:
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
        if keys[pygame.K_UP] and self.player.air_timer < 5 and not self.player.during_jump:
            self.player.y_speed -= JUMP_SPEED
            self.player.during_jump = True
            # self.sounds["jump"].play()
        # if keys[pygame.K_SPACE]:
        #     self.shoot()


    def check_hearts(self):
        if self.player.hp <= 0:
            self.end(f"Koniec gry, twój wynik punktowy: {self.points}")
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
            self.tiles_list.append(Tile((x * 30), 290, "wall"))
        for y in range(10):
            self.tiles_list.append(Tile(0, y * 32, "wall"))
            self.tiles_list.append(Tile(450, y * 32, "wall"))

        while True:
            self.current_time = pygame.time.get_ticks()

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

            # boom
            self.boom_life()
            self.boom_collision()

            # bonus
            self.bonus_collision()
            self.create_bonus()

            #tile
            self.create_tile()

            #points
            self.check_points()

            self.refresh_screen()
            self.draw()

    def end(self, text):
        self.end_txt = self.font_end.render(text, False,(255,0,0))
        self.surf_end = self.surf_points.get_rect(center=(60,160))
        empty_heart = Tile(0, 0, "heart_empty")
        self.draw_screen.blit(self.textures[empty_heart.tile_name], empty_heart)
        self.draw_screen.blit(self.end_txt,self.surf_end)
        # self.sounds['end_game'].play()
        self.refresh_screen()
        timer = END_TIME
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.close()

    def draw(self):
        self.draw_screen.blit(self.textures["background"],(0,0))
        self.draw_screen.blit(self.textures["player"],self.player)
        for tile in self.tiles_list:
            self.draw_screen.blit(self.textures[tile.tile_name], tile)
        for enemy in self.enemies_list:
            if isinstance(enemy,Bomb):
                if self.current_time - enemy.last_update >= enemy.animation_cooldown and (enemy.on_ground == True):
                    enemy.enemy_frame += 1
                    enemy.last_update = self.current_time
                    if enemy.enemy_frame >= 3:
                        enemy.enemy_frame = 1
                self.draw_screen.blit(self.textures[f"{enemy.enemy_name}{str(enemy.enemy_frame)}"], enemy)
            else:
                self.draw_screen.blit(self.textures[enemy.enemy_name], enemy)
        for bonus in self.bonus_list:
            self.draw_screen.blit(self.textures[bonus.bonus_name], bonus)
        for boom in self.boom_list:
            self.draw_screen.blit(self.textures[boom.enemy_name], boom)
        for heart in self.hearts_list:
            self.draw_screen.blit(self.textures[heart.tile_name], heart)
        self.draw_screen.blit(self.surf_points,self.points_txt)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled,(0,0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

Game()