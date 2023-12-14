import pygame, sys
import pygame.mixer
from auxiliar.constantes import (WHITE,screen_w,screen_h,open_configs)
from models.sound import Sound

class Pause(pygame.sprite.Sprite):
    def __init__(self, pos, stage_dict_configs: dict, sound_manager: Sound):
        super().__init__()
        
        self.pause_menu_path = stage_dict_configs.get('pause_menu')
        self.pause_menu = pygame.image.load(self.pause_menu_path)
        self.rect = self.pause_menu.get_rect(center=(screen_w//2, screen_h//2))

        self.font = pygame.font.Font(stage_dict_configs.get("font_title_path"), 40) 
        self.keys_text = self.font.render(f"PAUSE", True, WHITE)

        center_x = self.rect.centerx
        center_y = self.rect.centery

        text_rect = self.keys_text.get_rect(center=(center_x, center_y))
        self.text_pos = text_rect.topleft
        
        self.sound_manager = sound_manager
        self.volume = self.sound_manager.get_volume()
        
        self.pause_active = False

#    def handle_events(self):
#        keys = pygame.event.get()
#        if self.pause_active:
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_ESCAPE:
#                    self.pause_active = False
#                if event.key == pygame.K_RIGHT:
#                    self.subir_volumen(0.1)
#                if event.key == pygame.K_LEFT:
#                    self.bajar_volumen(0.1)

    def subir_volumen(self, nuevo_volumen):
        if self.volume <= 1:
            self.volume += nuevo_volumen
            self.sound_manager.set_volume(self.volume)

    def bajar_volumen(self, nuevo_volumen):
        if self.volume >= 0:
            self.volume -= nuevo_volumen
            self.sound_manager.set_volume(self.volume)

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.pause_menu, self.rect)
        screen.blit(self.keys_text,self.text_pos)




