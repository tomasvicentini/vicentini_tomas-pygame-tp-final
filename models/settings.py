import pygame

import random as rd
from auxiliar.constantes import (open_configs,screen_w,screen_h)
from models.pause import Pause

class Setting(pygame.sprite.Sprite):
    def __init__(self, screen, sound_config, font_menu):
        super().__init__()

        self.screen = screen
        self.sound_config = sound_config
        self.font = pygame.font.Font(font_menu,28)
        self.volume = self.sound_config['volume']
        self.showing = False

        self.__configs_menu = open_configs().get("menu")
        self.pause_menu_path = self.__configs_menu['pause_menu']
        self.image = pygame.image.load(self.pause_menu_path)
        self.rect = self.image.get_rect(center=(screen_w//2,screen_h//2))

    def render(self):
        pass

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.hide_config_screen()
                if event.key == pygame.K_RIGHT:
                    self.subir_volumen(0.1)
                if event.key == pygame.K_LEFT:
                    self.bajar_volumen(0.1)

    def subir_volumen(self,nuevo_volumen):
        if self.volume <= 1:
            self.sound_config['volume'] += nuevo_volumen
            pygame.mixer.set_volume(nuevo_volumen)

    def bajar_volumen(self,nuevo_volumen):
        if self.volume >= 0:
            self.sound_config['volume'] += nuevo_volumen
            pygame.mixer.set_volume(nuevo_volumen)

    def show_config_screen(self):
        self.showing = True

    def hide_config_screen(self):
        self.showing = False

    def update(self, screen: pygame.surface.Surface):
        self.screen.blit(self.image, self.rect)
    

        
        
