from auxiliar.constantes import (open_configs, GREEN, BLUE, WHITE, BLACK, RED)
import pygame,sys
from models.player import Player
from models.enemy import Enemy
from models.pause import Pause
from models.item import Item
from models.fire import Fire
from models.sound import Sound

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_w, limit_h, stage_name: str, puntaje):

        self.__player_win = False
        self.__player_lost = False
        self.__configs = open_configs().get(stage_name)

        # FONTS
        self.__configs_menu = open_configs().get("menu")
        self.__fonts = self.__configs_menu["font_menu_path"]
        self.__fonts_win = self.__configs_menu["font_title_path"]
        self.__fonts_text = self.__configs_menu["font_text_path"]
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

        self.sound_damage_path = self.__sounds['alien_scream']
        self.sound_damage = pygame.mixer.Sound(self.sound_damage_path)
        self.sound_damage.set_volume(self.__sounds['volume']*4)
        self.chanel_damage = pygame.mixer.Channel(5)

        #self.sound_damage_path = self.__sounds['you_bitch.WAV']
        #self.sound_damage = pygame.mixer.Sound(self.sound_damage_path)
        #self.sound_damage.set_volume(self.__sounds['volume']*4)
        #self.chanel_damage = pygame.mixer.Channel(5)

        # ITEM
        self.__configs_items = open_configs().get("item")
        self.item = pygame.sprite.Group()
        self.coordenadas_items = self.__stage_configs.get('coords_item')
        self.items_class = []
        self.spawnear_items()

        # FIRE
        self.fire = pygame.sprite.Group()
        self.coordenadas_fire = self.__stage_configs.get('coords_fire')
        self.fire_class = []
        self.spawnear_fire()
        
        # TIME
        self.tiempo_limite = 60
        self.tiempo = 60
        self.tiempo_inicial = pygame.time.get_ticks() // 1000
        self.tiempo_transcurrido = 0
        
        # PAUSE
        self.pause = False
        self.sound_manager = Sound()
        self.pause_menu = Pause((0, 532), self.__configs_menu,self.sound_manager)

        self.enemies_class = []
        self.spawnear_enemigos()

        self.puntaje = puntaje

        for enemy in self.enemies_class:
            self.enemies.add(enemy)
    
    def pause_enemies(self):
        for enemy in self.enemies_class:
            enemy.pause = True

    def resume_enemies(self):
        for enemy in self.enemies_class:
            enemy.pause = False

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

    def spawnear_items(self):
        for coor in self.coordenadas_items:
            item_instance = Item(coor.get("coord_x"), coor.get("coord_y"), self.__configs_items, self.__sounds)
            self.item.add(item_instance)
            self.items_class.append(item_instance)

    def spawnear_fire(self):
        for coor in self.coordenadas_fire:
            fire_instance = Fire(coor.get("coord_x"), coor.get("coord_y"), self.__configs_items, self.__sounds)
            self.fire.add(fire_instance)
            self.fire_class.append(fire_instance)

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
        font_score = pygame.font.Font(self.__fonts_text, 28)
        score_text = font_score.render(f"Score: {self.puntaje}", True, WHITE)
        self.__main_screen.blit(score_text, (10, 10))

        # MENSAJE DE MUNICION
        font_ammo = pygame.font.Font(self.__fonts_text, 28)
        ammo_text = font_ammo.render(f"Ammo: {self.player_sprite.municion}", True, WHITE)
        self.__main_screen.blit(ammo_text, (10, 50))

        # MENSAJE DE VIDA DEL PLAYER
        font_health = pygame.font.Font(self.__fonts_text, 28)
        score_health = font_health.render(f"Vida: {self.player_sprite.health}", True, WHITE)
        self.__main_screen.blit(score_health, (300, 10))

        # MENSAJE DE TIEMPO
        #font_time = pygame.font.Font(self.__fonts_text, 28)
        #score_time = font_time.render(f"Time: {self.tiempo}", True, WHITE)
        #self.__main_screen.blit(score_time, (self.__limit_w - self.__limit_w/4.3, 10))
        
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
            lost_text = font.render(f"nivel fallido", True, WHITE)
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
                        self.puntaje += 100
                        print(f'Puntaje actual: {self.player_sprite.puntaje} Puntos')                   

        all_enemies_killed = all(enemy.killed for enemy in self.enemies)
        if all_enemies_killed and not self.__player_win:
            self.__player_win = True
            print(f'Ganaste la partida con: {self.player_sprite.puntaje} Puntos!')

    def colission_player_items(self):
        items_hit = pygame.sprite.spritecollide(self.player_sprite, self.item, True)
        for item in items_hit:
            item.colision = True
            print("Colisión con item")
            if self.player_sprite.municion <= 30:
                self.player_sprite.municion = 30
            elif self.player_sprite.municion <= 60: 
                self.player_sprite.municion = 60

    def colission_player_fire(self):
        fire_hit = pygame.sprite.spritecollide(self.player_sprite, self.fire, False)
        for fire in fire_hit:
            fire.colision = True
            print("Colisión con fire")
            self.player_sprite.health -= 5

    def colission_enemy_player(self):
        enemies_hit = pygame.sprite.spritecollide(self.player_sprite, self.enemies, False)
        for enemy in enemies_hit:
            if not enemy.killed:
                if not self.player_sprite.is_dead:
                    self.chanel_damage.play(self.sound_damage)
                    self.sound_destruct.stop()
                self.player_sprite.health -= 15
            if self.player_sprite.health <= 0:
                self.player_sprite.health = 0
                self.player_sprite.is_dead = True

        if self.player_sprite.is_dead and not self.__player_lost:
            self.__player_lost = True
            print(f'Perdiste la partida con: {self.player_sprite.puntaje} Puntos!')

    #def temporizador(self):
    #    tiempo_actual = 0
    #    if not self.__player_win and not self.__player_lost:
    #        if not self.pause:
    #            tiempo_actual = pygame.time.get_ticks() // 1000
    #            self.tiempo = self.tiempo_limite - tiempo_actual
#
    #            if self.tiempo <= 0:
    #                self.__player_lost = True
    #                self.tiempo = 0
#
    #    if not self.pause:
    #        self.tiempo_inicial = tiempo_actual
#
    #    print(f"{self.tiempo} - {self.tiempo_inicial} - {tiempo_actual}")

    def run(self, delta_ms):
        #DIBUJAR PISOS
        for floor_rect in self.floor_class:
            pygame.draw.rect(self.__main_screen, BLACK, floor_rect, 2)

        #DIBUJAR ESCALERAS
        for ladder_rect in self.ladders_class:
            pygame.draw.rect(self.__main_screen, BLACK, ladder_rect, 2)
        
        for item in self.items_class:
            if not item.colision:
                item.update(self.__main_screen)
                #pygame.draw.rect(self.__main_screen, BLACK, item, 2)

        for fire in self.fire_class:
            fire.update(delta_ms,self.__main_screen)
            #pygame.draw.rect(self.__main_screen, BLACK, fire, 2)
        if self.stage_name != 'win':
            self.player.update(self.__main_screen,self.pause)
            self.player.draw(self.__main_screen)
            self.enemies.update(delta_ms, self.__main_screen,self.pause)
            if not self.sound_is_running:
                self.destruct_sequence()
                self.sound_is_running = True
        
        #self.temporizador()
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not self.pause:
                    self.pause = True
                    self.pause_menu.pause_active = True
                    self.pause_enemies()
                else:
                    self.pause = False
                    self.pause_menu.pause_active = False
                    self.resume_enemies()
        
        if self.pause:
            self.pause_menu.draw(self.__main_screen)
            self.pause_enemies()
            self.pause_menu.pause_active = True
        elif not self.pause or not self.__player_lost:
            self.colission_bullet_enemy()
            self.colission_enemy_player()
            self.colission_player_items()
            self.colission_player_fire()
            self.resume_enemies()
            #self.pause_menu.pause_active = False

        if self.stage_name != 'win':
            self.score_puntaje()

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

        pygame.display.flip()