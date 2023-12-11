import pygame
from pygame.locals import *
import sys
from models.GUI_form_prueba import FormPrueba
from models.stage import Stage
from auxiliar.constantes import (screen_h, screen_w, open_configs, FPS, GREY)

class Game:
    def __init__(self) -> None:
        self.__game_configs = open_configs().get('menu')
        self.background_path = self.__game_configs.get("background_menu")
        self.background = pygame.image.load(self.background_path)
        self.background = pygame.transform.scale(self.background,(screen_w,screen_h))
        
        # ICONO
        pygame.init()
        pygame.display.set_caption("Alien Shooter")
        icono = pygame.image.load("./assets/graphics/menu/icon.png")
        pygame.display.set_icon(icono)

        self.screen = pygame.display.set_mode((screen_w, screen_h))
       
       # SONIDOS
        self.__sounds = open_configs().get('sounds')
        self.sound_menu_path = self.__sounds['ambient']
        self.sound_menu = pygame.mixer.Sound(self.sound_menu_path)
        self.sound_menu.set_volume(self.__sounds['volume']*2)
        
        # NIVELES
        self.current_stage = "menu"
        self.stage_enable = [True,False,False]

    def menu(self):
        self.sound_menu.play()
        font_title_path = self.__game_configs.get('font_title_path')
        font_titulo = pygame.font.Font(font_title_path,42)
        txt_titulo = font_titulo.render("ALiEN SHOOTER", True, "white")
        pos_txt_titulo = ((screen_w - txt_titulo.get_width()) // 2, screen_h / 6)

        # FUENTE PARA EL MENÚ
        font_menu_path = self.__game_configs.get('font_menu_path')
        font_menu = pygame.font.Font(font_menu_path, 28)
        opciones_menu = ["NIVEL 1", "NIVEL 2", "NIVEL 3"]
        textos_menu = []
        for i, opcion in enumerate(opciones_menu):
            if self.stage_enable[i]:
                texto_opcion = font_menu.render(opcion, True, "white") 
            else:
                texto_opcion = font_menu.render(opcion, True, GREY) 
            textos_menu.append(texto_opcion)
        # Posicion para el menu
        pos_x_menu = (screen_w - textos_menu[0].get_width()) // 6
        pos_y_menu = screen_w / 2.5
        espacio_entre_opciones = 200   

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == MOUSEBUTTONDOWN:
                    for i, texto_opcion in enumerate(textos_menu):
                        opcion_rect = texto_opcion.get_rect(topleft=(pos_x_menu + i * espacio_entre_opciones, pos_y_menu))
                        if opcion_rect.collidepoint(evento.pos):
                            if i == 0:
                                self.sound_menu.stop()
                                self.current_stage = "stage_1"
                                #self.run_stage("stage_1")
                            elif i == 1 and self.stage_enable[1]:
                                self.sound_menu.stop()
                                self.current_stage = "stage_2"
                                #self.run_stage("stage_2")
                            elif i == 2 and self.stage_enable[2]:
                                self.sound_menu.stop()
                                self.current_stage = "stage_3"
                                #self.run_stage("stage_3")

            if self.current_stage == "menu":
                self.screen.blit(self.background,(0,0))
                self.screen.blit(txt_titulo,pos_txt_titulo)
                for i, texto_opcion in enumerate(textos_menu):
                    if self.stage_enable[i]:
                        self.screen.blit(texto_opcion,(pos_x_menu + i * espacio_entre_opciones, pos_y_menu))
            
                pygame.display.flip()
            else:
                self.run_stage(self.current_stage)

    def player_win_every_stage(self):
        # SONIDOS
        sound_winner_path = self.__sounds['winner']
        sound_winner = pygame.mixer.Sound(sound_winner_path)
        sound_winner.set_volume(self.__sounds['volume']*2)
        sound_winner.play()
        # FONTS
        font = pygame.font.Font(self.__game_configs.get('font_title_path'), 28)
        score_text = font.render(f"felicitaciones, completaste el juego", True, "white")
        self.screen.blit(score_text, (screen_w / 8, screen_h / 2))    

        stage_config = open_configs().get("win")
        background_path = stage_config.get("background_img")   
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background,(screen_w,screen_h))
        screen = pygame.display.set_mode((screen_w, screen_h))

        screen.blit(background, (0, 0))

    def flow_stages(self):
        print("entre a flow")
        if self.current_stage == 'stage_1':
            print(f"FLOW-STAGE-1{self.current_stage}")
            self.stage_enable[1] = True
            self.current_stage = 'stage_2'
        elif self.current_stage == 'stage_2':
            print("FLOW-STAGE-2")
            self.stage_enable[2] = True
            self.current_stage = 'stage_3'
        elif self.current_stage == 'stage_3':
            print("FLOW-STAGE-3")
            self.player_win_every_stage()
            self.current_stage = 'win'
        elif self.current_stage == 'win':
            print("FLOW-WIN")
            self.current_stage == 'menu'


    def run_stage(self, stage_name):

        # Obtener la configuración de la etapa actual desde el JSON
        stage_config = open_configs().get(stage_name)
        background_path = stage_config.get("background_img")

        # Cargar la imagen de fondo
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background,(screen_w,screen_h))

        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        game_stage = Stage(screen, screen_w, screen_h, stage_name)  


        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if game_stage._Stage__player_win and self.current_stage != 'win':
                #game_stage.sound_destruct.stop()

                if keys[pygame.K_SPACE]:
                    self.flow_stages()
                    return
            elif game_stage._Stage__player_lost or self.current_stage == 'win':
                game_stage.sound_destruct.stop()

                if keys[pygame.K_SPACE]:
                    self.current_stage = "menu"
                    return      

            screen.blit(background, (0, 0))

            delta_ms = clock.tick(FPS)
            game_stage.run(delta_ms)
            pygame.display.flip()

