import pygame
import sys
from models.stage import Stage
from auxiliar.constantes import (screen_h, screen_w, open_configs)

class Game:
    def __init__(self) -> None:
        pass

    def run_stage(self, stage_name: str):
        pygame.init()

        # Obtener la configuración de la etapa actual desde el JSON
        stage_config = open_configs().get(stage_name)
        background_path = stage_config.get("background_img")

        # Cargar la imagen de fondo
        background = pygame.image.load(background_path)
        
        screen = pygame.display.set_mode((screen_w, screen_h))
        clock = pygame.time.Clock()
        game = Stage(screen, screen_w, screen_h, stage_name)  # Pasar el fondo como parámetro
        #game = Game(screen_w, screen_h, "stage_2")  # instancia de la clase

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(background, (0, 0))  # Usar blit para dibujar el fondo
            delta_ms = clock.tick(30)
            game.run(delta_ms)
            pygame.display.flip()
