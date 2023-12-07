from auxiliar.constantes import (open_configs, GREEN, BLUE)
import pygame
from models.player import Player
from models.enemy import Enemy

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):

        self.__configs = open_configs().get(stage_name)
        
        # Pisos
        self.floor = self.__configs["floor"]
        self.on_floor = False
        self.floor_class = []
        self.spawnear_floor()

        # Escaleras
        self.ladders = self.__configs["ladders"]
        self.on_ladder = False
        self.ladders_class = []
        self.spawnear_ladders()

        # Jugador
        player_coords = self.__configs.get('player').get('coord_player')[0]
        self.player_sprite = Player((player_coords.get("coord_x"), player_coords.get("coord_y")), limit_w, self.__configs) # posicion inicial
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

    def spawnear_ladders(self):
        for ladder in self.ladders:
            ladder_rect = pygame.Rect(ladder.get("x"),ladder.get("y"),ladder.get("w"),ladder.get("h"))
            self.ladders_class.append(ladder_rect)

    def spawnear_floor(self):
        for floor in self.floor:
            floor_rect = pygame.Rect(floor.get("x"),floor.get("y"),floor.get("w"),floor.get("h"))
            self.floor_class.append(floor_rect)

    def run(self, delta_ms):
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

        #DIBUJAR PISOS
        for floor_rect in self.floor_class:
            pygame.draw.rect(self.__main_screen, BLUE, floor_rect, 2)

        #for floor_rect in self.floor_class:
        #    if self.player_sprite.rect.colliderect(floor_rect):
        #        self.player_sprite.on_floor = True
        #        break
        #else:
        #    self.player_sprite.on_floor = True

        #DIBUJAR ESCALERAS
        for ladder_rect in self.ladders_class:
            pygame.draw.rect(self.__main_screen, GREEN, ladder_rect, 2)

        for ladder_rect in self.ladders_class:
            if self.player_sprite.rect.colliderect(ladder_rect):
                self.player_sprite.on_ladder = True
                break
        else:
            self.player_sprite.on_ladder = False
            self.player_sprite.lock_ladder = False

        # Verificar si el jugador está en el suelo   
        ground_level = self.__limit_h - self.player_sprite.rect.height
        if self.player_sprite.rect.y > ground_level:
            self.player_sprite.rect.y = ground_level
            #self.player_sprite.is_jumping = False
            self.player_sprite.y_speed = 0  # Detener la velocidad vertical cuando está en el suelo
            self.player_sprite.lock_ladder = False

        for floor_rect in self.floor_class:
            self.player_sprite.handle_vertical_collision(floor_rect, self.ladders_class, self.player_sprite.y_speed)

        