import pygame
from pygame.locals import *
import sys
from models.GUI_form_prueba import FormPrueba
from models.stage import Stage
from auxiliar.constantes import (screen_h, screen_w, open_configs, FPS)

class Game:
    def __init__(self) -> None:
        self.__game_configs = open_configs().get('menu')

    def run_stage(self):
        pygame.init()

        # ICONO
        pygame.display.set_caption("Alien Shooter")
        icono = pygame.image.load("./assets/graphics/menu/icon.png")
        pygame.display.set_icon(icono)

        #################################################################
        # TITULO
        '''
        font_title_path = self.__game_configs.get('font_title_path')
        font_titulo = pygame.font.Font(font_title_path,35)
        txt_titulo = font_titulo.render("ALiEN SHOOTER", True, "white")
        pos_txt_titulo = ((screen_w - txt_titulo.get_width()) // 2, 35)

        # FUENTE PARA EL MENÚ
        font_menu_path = self.__game_configs.get('font_menu_path')
        font_menu = pygame.font.Font(font_menu_path, 20)
        opciones_menu = ["Iniciar", "Opciones", "Salir"]
        textos_menu = [font_menu.render(opcion, True, "white") for opcion in opciones_menu]

        # Posicion para el menu
        pos_x_menu = (screen_w - textos_menu[0].get_width()) // 2
        pos_y_menu = 200
        espacio_entre_opciones = 50        
        '''
        #################################################################
        
        stage_name = 'stage_1'

        # Obtener la configuración de la etapa actual desde el JSON
        stage_config = open_configs().get(stage_name)
        background_path = stage_config.get("background_img")

        # Cargar la imagen de fondo
        background = pygame.image.load(background_path)
        
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        game = Stage(screen, screen_w, screen_h, stage_name)  # Pasar el fondo como parámetro
        #game = Game(screen_w, screen_h, "stage_2")  # instancia de la clase

        form_prueba = FormPrueba(screen,0,0, screen_w, screen_h,"black", "yellow", 5, True)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            screen.blit(background, (0, 0))  # Usar blit para dibujar el fondo

            #form_prueba.update(pygame.event.get())

            #screen.blit(txt_titulo, pos_txt_titulo)
            # Dibuja las opciones del menú en la pantalla
            #for i, texto_opcion in enumerate(textos_menu):
            #    screen.blit(texto_opcion, (pos_x_menu, pos_y_menu + i * espacio_entre_opciones))
            delta_ms = clock.tick(FPS)
            game.run(delta_ms)
            pygame.display.flip()
