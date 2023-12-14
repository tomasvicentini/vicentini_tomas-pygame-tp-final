import pygame

import random as rd
from auxiliar.constantes import (WHITE,screen_h,screen_w,BLACK)

class Item(pygame.sprite.Sprite):
    def __init__(self, posx, posy, __item: dict, __sounds: dict):
        super().__init__()

        self.image_path = __item['item_ammo']
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.original_image, (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        #self.rect = self.image.get_rect(center=(posx, posy))
       
        # SONIDOS
        self.sound = __sounds['pickup_ammo']
        self.sound_ammo = pygame.mixer.Sound(self.sound)
        self.sound_ammo.set_volume(__sounds['volume'] * 2)
        self.colision = False

    def update(self, screen: pygame.surface.Surface):
        if self.colision:
            chanel_ammo = pygame.mixer.Channel(1)
            chanel_ammo.play(self.sound_ammo)
            print("sonido ammo")
            self.colision = False
            self.kill()
        else:
            screen.blit(self.image, self.rect)
    

        
        
