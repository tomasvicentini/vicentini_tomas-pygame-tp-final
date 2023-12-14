import pygame

import random as rd
from auxiliar.constantes import (WHITE,screen_h,screen_w,BLACK)

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, __item: dict, __sounds: dict):
        super().__init__()

        #self.image_path = __item['fire']
        self.fire_images = [pygame.image.load(image).convert_alpha() for image in __item['fire']]
        self.image = pygame.transform.scale(self.fire_images[0], (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animacion
        self.animacion_contador = 0
        self.animation_speed = 5
       
        # SONIDOS
        self.sound = __sounds['fire_shoot']
        self.sound_fire = pygame.mixer.Sound(self.sound)
        self.sound_fire.set_volume(__sounds['volume'] * 2)
        self.colision = False

        self.sound_player = __sounds['damage_player']
        self.sound_player_damage = pygame.mixer.Sound(self.sound_player)
        self.sound_player_damage.set_volume(__sounds['volume'] * 2)


    def movement(self, delta_ms):
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed)
        self.image = self.fire_images[self.animacion_contador // self.animation_speed]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(WHITE)


    def update(self, delta_ms, screen: pygame.surface.Surface):
        self.movement(delta_ms)
        screen.blit(self.image, self.rect)
        
        if self.colision:
            chanel_fire = pygame.mixer.Channel(1)
            chanel_player_damage = pygame.mixer.Channel(2)
            if not chanel_fire.get_busy():
                chanel_fire.play(self.sound_fire)
                print("sonido fire")
                chanel_fire.play(self.sound_fire)
            if not chanel_player_damage.get_busy():
                print("sonido damage")
                chanel_player_damage.play(self.sound_player_damage)
            self.colision = False
        
    

        
        
