import pygame.mixer
from auxiliar.constantes import (open_configs)

class Sound:
    def __init__(self):
        pygame.mixer.init()
        
        self.__sounds = open_configs().get('sounds')
        self.volume =self.__sounds['volume']
    
    def set_volume(self, new_volume):
        if 0 <= new_volume <= 1:
            self.volume = new_volume
            pygame.mixer.music.set_volume(new_volume)
            print(self.volume)

    def get_volume(self):
        return self.volume
