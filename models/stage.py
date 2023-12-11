from auxiliar.constantes import (open_configs, GREEN, BLUE, WHITE, BLACK, RED)
import pygame
from models.player import Player
from models.enemy import Enemy

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str):

        self.__player_win = False
        self.__player_lost = False
        self.__configs = open_configs().get(stage_name)
        self.__configs_menu = open_configs().get("menu")
        self.__fonts = self.__configs_menu["font_menu_path"]
        self.__fonts_win = self.__configs_menu["font_title_path"]
        self.stage_name = stage_name

        # SONIDOS
        self.__sounds = open_configs().get('sounds')
        self.sound_destruct_path = self.__sounds['destruct_sequence']
        self.sound_destruct = pygame.mixer.Sound(self.sound_destruct_path)
        self.sound_destruct.set_volume(self.__sounds['volume']*2)
        self.sound_is_running = False

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

    def destruct_sequence(self):
        self.sound_destruct.play()

    def score_puntaje(self):
        # MENSAJE DE PUNTAJE
        font_score = pygame.font.Font(self.__fonts, 20)
        score_text = font_score.render(f"Puntaje: {self.player_sprite.puntaje}", True, WHITE)
        self.__main_screen.blit(score_text, (10, 10))

        # MENSAJE DE VIDA DEL PLAYER
        font_health = pygame.font.Font(self.__fonts, 20)
        score_health = font_health.render(f"Vida: {self.player_sprite.health}", True, WHITE)
        self.__main_screen.blit(score_health, (10, 40))
        
        # MENSAJE DE NIVEL COMPLETADO
        if self.__player_win and self.stage_name != "win":
            #self.__main_screen.fill(BLACK)
            font = pygame.font.Font(self.__fonts_win, 32)
            win_text = font.render(f"nivel  completado", True, WHITE)
            self.__main_screen.blit(win_text, (self.__limit_w / 8, self.__limit_h / 2))

            font_menu = pygame.font.Font(self.__fonts, 12) 
            keys_text = font_menu.render(f"press SPACE", True, "white")
            self.__main_screen.blit(keys_text, (self.__limit_w / 2.5, self.__limit_h / 1.8))  

        # MENSAJE DE NIVEL FALLIDO
        if self.__player_lost:
            #self.__main_screen.fill(BLACK)
            font = pygame.font.Font(self.__fonts_win, 32)
            lost_text = font.render(f"has  muerto", True, WHITE)
            self.__main_screen.blit(lost_text, (self.__limit_w / 4, self.__limit_h / 2))

            font_menu = pygame.font.Font(self.__fonts, 12) 
            keys_text = font_menu.render(f"press SPACE", True, "white")
            self.__main_screen.blit(keys_text, (self.__limit_w / 2.5, self.__limit_h / 1.8))    

    def colission_bullet_enemy(self):
        for bullet in self.player_sprite.get_bullets:
            enemies_hit = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in enemies_hit:
                if not enemy.killed:
                    enemy.health -= 1
                    if enemy.health >= 0: bullet.kill()
                    if enemy.health <= 0:
                        enemy.killed = True
                        self.player_sprite.puntaje += 100
                        print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')                   

        all_enemies_killed = all(enemy.killed for enemy in self.enemies)
        if all_enemies_killed and not self.__player_win:
            self.__player_win = True
            print(f'Ganaste la partida con: {self.player_sprite.puntaje} Puntos!')

    def colission_enemy_player(self):
        enemies_hit = pygame.sprite.spritecollide(self.player_sprite, self.enemies, False)
        for enemy in enemies_hit:
            if not enemy.killed:
                self.player_sprite.health -= 15
            if self.player_sprite.health <= 0:
                self.player_sprite.health = 0
                self.player_sprite.is_dead = True

        if self.player_sprite.is_dead and not self.__player_lost:
            self.__player_lost = True
            print(f'Perdiste la partida con: {self.player_sprite.puntaje} Puntos!')

    def run(self, delta_ms):
        self.player.update(self.__main_screen)
        self.player.draw(self.__main_screen)
        self.enemies.update(delta_ms, self.__main_screen)
        if not self.sound_is_running:
            self.destruct_sequence()
            self.sound_is_running = True
        self.score_puntaje()
        self.colission_bullet_enemy()
        self.colission_enemy_player()
        
        #DIBUJAR PISOS
        for floor_rect in self.floor_class:
            pygame.draw.rect(self.__main_screen, BLACK, floor_rect, 2)

        #DIBUJAR ESCALERAS
        for ladder_rect in self.ladders_class:
            pygame.draw.rect(self.__main_screen, BLACK, ladder_rect, 2)

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
            self.player_sprite.y_speed = 0  
            self.player_sprite.lock_ladder = False

        for floor_rect in self.floor_class:
            self.player_sprite.handle_vertical_collision(floor_rect, self.ladders_class, self.player_sprite.y_speed)
    

        