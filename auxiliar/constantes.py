import json
import pygame


#pygame.init()
#screen_info = pygame.display.Info()
#screen_w = screen_info.current_w
#screen_h = screen_info.current_h

screen_w = 736
screen_h = 858

FPS= 30

#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (222,222,222)

CONFIG_FILE_PATH = './configs/config.json'


def open_configs() -> dict:
    with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as config:
        return json.load(config)
