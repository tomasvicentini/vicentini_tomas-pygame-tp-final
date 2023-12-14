import pygame

import random as rd
from models.Bullet import Bullet
from auxiliar.constantes import (WHITE,open_configs)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, stage_dict_configs: dict):
        super().__init__()

        self.__enemy_configs = stage_dict_configs.get('enemy')

        # SONIDOS
        self.__sounds = open_configs().get('sounds')
        self.sound_dead_alien_path = self.__sounds['dead_alien']
        self.sound_dead = pygame.mixer.Sound(self.sound_dead_alien_path)
        self.sound_dead.set_volume(self.__sounds['volume'] * 2)

        # Mostrar sprite del enemigo
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__enemy_configs['run_img']]
        self.dead_images = [pygame.image.load(image).convert_alpha() for image in self.__enemy_configs['dead_img']]
        self.image_index = 0
        self.image = self.move_images[self.image_index]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(midbottom=pos)

        # Atributos de movimiento
        self.__setear_velocidad()
        self.max_x_constraint = constraint_x
        self.max_y_constraint = constraint_y
        self.frame_rate = 200
        self.time_move = 0
        self.animation_speed = 3
        self.animation_dead = 1
        self.animacion_contador = 0
        self.move_right = True
        self.bullet_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        self.health = self.__enemy_configs['health']
        self.is_dead = False
        self.killed = False
        self.pause = False
 
    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.move_right:
            if (self.rect.right + self.speed ) < self.max_x_constraint:
                self.rect.x += self.speed
            else:
                self.move_right = False
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
        else:
            if self.rect.left - self.speed > 0:
                self.rect.x -= self.speed
                self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
            else:
                self.move_right = True
                self.image = pygame.transform.flip(self.image, False, False)
                self.image.set_colorkey(WHITE)
        
    def __setear_velocidad(self):
        self.speed = rd.randint(self.__enemy_configs['min_enemy_speed'], self.__enemy_configs['max_enemy_speed'])

    def do_movement(self, delta_ms):
        self.time_move += delta_ms
        if self.time_move >= self.frame_rate:
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed)
            self.image = self.move_images[self.animacion_contador // self.animation_speed]
            self.image.set_colorkey(WHITE)
            self.constraint()

    def do_dead(self,delta_ms):
        self.time_move += delta_ms
        if self.animacion_contador == len(self.dead_images)-1:
            if self.move_right:
                self.image = self.dead_images[-1]   
            else: 
                self.image = pygame.transform.flip(self.dead_images[-1], True, False)
            self.image.set_colorkey(WHITE)     
        elif self.time_move >= self.frame_rate:
            if self.animacion_contador < len(self.dead_images) * self.animation_dead:
                self.image = self.dead_images[self.animacion_contador // self.animation_dead]
                if not self.move_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
                self.animacion_contador += 1
            else:
                self.animacion_contador = 0
                self.time_move = 0

    def update(self, delta_ms, screen: pygame.surface.Surface, pause):
        if self.health > 0 and not self.pause:
            self.do_movement(delta_ms)
            self.draw(screen)
            self.clock.tick(60)
        elif pause:
            self.draw(screen)
        else:
            self.do_dead(delta_ms)
            self.draw(screen)
            self.clock.tick(60)
            if not self.is_dead:
                chanel_dead = pygame.mixer.Channel(6)
                chanel_dead.play(self.sound_dead)
                self.is_dead = True
    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
        
