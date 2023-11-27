from auxiliar.constantes import (open_configs)
import pygame
from models.player import Player
from models.enemy import Enemy

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):

        # Jugador
        self.__configs = open_configs().get(stage_name)
        self.player_sprite = Player((limit_w / 2, limit_h),limit_w, self.__configs)  # posicion inicial
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.enemies = pygame.sprite.Group()
        self.__stage_configs = self.__configs.get('stage')
        self.__max_enemies = self.__stage_configs["max_amount_enemies"]
        self.__player_win = False
        self.__coordenadas_enemigos = self.__stage_configs.get("coords_enemies")
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        self.__main_screen = screen
        
        self.enemies_class = []
        self.spawnear_enemigos()



        for enemy in self.enemies_class:
            self.enemies.add(enemy)

    def spawnear_enemigos(self):
        if self.__max_enemies > len(self.__coordenadas_enemigos):
            for coordenada in self.__coordenadas_enemigos:
                self.enemies_class.append(
                    Enemy((coordenada.get("coord_x"), coordenada.get("coord_y")), 
                    self.__limit_w, self.__limit_h, self.__configs)
                )
        elif self.__max_enemies <= len(self.__coordenadas_enemigos):
            for coordenada in range(self.__max_enemies):
                self.enemies_class.append(
                    Enemy((self.__coordenadas_enemigos[coordenada].get("coord_x"), 
                           self.__coordenadas_enemigos[coordenada].get("coord_y")), 
                    self.__limit_w, self.__limit_h, self.__configs)
                )


    def run(self, delta_ms):
        # Actualizar todos los grupos de sprites
        # Dibujar todos los grupos de sprites

        # Actualizar y Dibujar Jugador
        self.player.update(self.__main_screen)
        self.player.draw(self.__main_screen)
        self.enemies.update(delta_ms, self.__main_screen)
        
        #self.enemies.draw(screen)
        
        for bullet in self.player_sprite.get_bullets:
            cantidad_antes = len(self.enemies)
            pygame.sprite.spritecollide(bullet, self.enemies, True)
            cantidad_despues = len(self.enemies)
            if cantidad_antes > cantidad_despues:
                cantidad_vencido = cantidad_antes - cantidad_despues
                self.player_sprite.puntaje += cantidad_vencido * 100
                print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')
            if len(self.enemies) == 0 and not self.__player_win:
                self.__player_win = True
                print(f'Ganaste la partida con: {self.player_sprite.puntaje} Puntos!')
