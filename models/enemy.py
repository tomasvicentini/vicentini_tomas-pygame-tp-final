import pygame
import random as rd
from models.Bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, stage_dict_configs: dict):
        super().__init__()

        self.__enemy_configs = stage_dict_configs.get('enemy')
        self.__percentaje_shoot = self.__enemy_configs["percentaje_shoot"]

        # Mostrar sprite del jugador
        self.avatar = self.seleccionar_avatar()
        self.image = pygame.image.load(self.__enemy_configs["enemy_img"].format(self.avatar)).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

        # Atributos de movimiento
        self.__setear_velocidad()
        self.max_x_constraint = constraint_x
        self.max_y_constraint = constraint_y
        self.frame_rate = 120
        self.time_move = 0
        self.move_right = True
        self.bullet_group = pygame.sprite.Group()

    
    def seleccionar_avatar(self):
        avatar = rd.choice(['Alien','Alien_crouch'])
        return avatar
    
    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.move_right:
            if (self.rect.right + self.speed ) < self.max_x_constraint:
                #self.rect.left += self.speed
                self.rect.x += self.speed
            else:
                self.move_right = False
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            if self.rect.left - self.speed > 0:
                #self.rect.right -= self.speed
                self.rect.x -= self.speed
            else:
                self.move_right = True
                self.image = pygame.transform.flip(self.image, True, False)
        
    def __setear_velocidad(self):
        self.speed = rd.randint(self.__enemy_configs["min_enemy_speed"], self.__enemy_configs["max_enemy_speed"])

    def do_movement(self, delta_ms):
        self.time_move += delta_ms
        if self.time_move >= self.frame_rate:
            self.constraint()

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        self.draw(screen)

    
    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
