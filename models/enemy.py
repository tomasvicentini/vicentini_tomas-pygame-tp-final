import pygame
import random as rd
from models.Bullet import Bullet
from auxiliar.constantes import WHITE

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_x, constraint_y, stage_dict_configs: dict):
        super().__init__()

        self.__enemy_configs = stage_dict_configs.get('enemy')

        # Mostrar sprite del enemigo
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__enemy_configs['run_img']]
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
        self.move_right = True
        self.bullet_group = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
 
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
            self.image_index = (self.image_index + 1) % len(self.move_images)
            self.image = self.move_images[self.image_index]
            self.image.set_colorkey(WHITE)
            self.constraint()

    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.do_movement(delta_ms)
        self.draw(screen)
        self.clock.tick(60)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)
