import pygame
import pygame.mixer
from models.Bullet import Bullet
from auxiliar.constantes import (open_configs,FPS, WHITE)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, stage_dict_configs: dict):
        super().__init__()
        pygame.mixer.init()
        
        self.__player_configs = stage_dict_configs.get('player')

        # SONIDOS
        self.__sounds = open_configs().get('sounds')
        self.sound_gun_path = self.__sounds['gun']
        self.sound_gun = pygame.mixer.Sound(self.sound_gun_path)
        self.sound_gun.set_volume(self.__sounds['volume'])
        self.chanel_gun = pygame.mixer.Channel(3)

        self.sound_gun_empty_path = self.__sounds['gun_empty']
        self.sound_gun_empty = pygame.mixer.Sound(self.sound_gun_empty_path)
        self.sound_gun_empty.set_volume(self.__sounds['volume'])
        
        self.sound_ladder_path = self.__sounds['ladder']
        self.sound_ladder = pygame.mixer.Sound(self.sound_ladder_path)
        self.sound_ladder.set_volume(self.__sounds['volume']*2)
        self.chanel_ladder = pygame.mixer.Channel(2)

        self.sound_steps_path = self.__sounds['steps']
        self.sound_steps = pygame.mixer.Sound(self.sound_steps_path)
        self.sound_steps.set_volume(0)
        self.chanel_steps = pygame.mixer.Channel(1)

        self.sound_dead_path = self.__sounds['dead']
        self.sound_dead = pygame.mixer.Sound(self.sound_dead_path)
        self.sound_dead.set_volume(self.__sounds['volume']*2)
        self.chanel_dead = pygame.mixer.Channel(4)
        self.scream = True
              
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['run_img']] # Sprite player run
        self.idle_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['idle_img']] # Sprite player iddle
        self.fire_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['fire_img']] # Sprite player fire
        self.jump_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['jump_img']] # Sprite player jump
        self.up_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['up_img']] # Sprite player up
        self.dead_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['dead_img']] # Sprite player dead

        # Establecer la imagen actual
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.original_image = self.image
 
        # Atributos de movimiento
        self.speed = self.__player_configs['speed']
        
        self.max_x_constraint = constraint
        
        #NUEVOS METODOS
        self.direction = self.__player_configs["direction"]
        #self.animation_count = 0
        self.x_vel = 0
        self.y_speed = 0
        self.is_moving = False
        self.space_pressed = False
        self.up_pressed = False
        self.move_pressed = False
        self.on_ladder_floor = False
        self.on_ground = False
        self.animacion_contador = 0
        self.animation_speed_idle = 30
        self.animation_speed_fire = 15
        self.animation_speed_move = 5
        self.animation_speed_jump = 5
        self.animation_speed_up = 1
        self.animation_dead = 1

        # GRAVEDAD - SALTO
        self.fall_count = 0
        self.gravity = 1.8
        self.jump_count = 0
        self.jump_height = 3
        self.is_jumping = False
        
        #self.is_jumping = False
        self.speed_jump = self.__player_configs['speed_jump']
        self.speed_ladder = self.__player_configs['speed_ladder']

        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.bullet_group = pygame.sprite.Group()
        self.puntaje = 0

        # Pisos
        self.on_floor = False
        self.floor_class = []

        # Escaleras
        self.on_ladder = False
        self.lock_ladder = False

        # Vida
        self.health = 100
        self.is_dead = False

        # Municion
        self.municion = 30
        self.pause = False

    @property
    def get_bullets(self) -> list[Bullet]:
        return self.bullet_group
    
    def shoot_laser(self):  # disparar laser
        self.bullet_group.add(self.create_bullet())

    def create_bullet(self):
        self.municion -= 1
        return Bullet(self.rect.centerx, self.rect.top+17, self.direction, True)
        
    def recharge(self):
        if not self.ready:
            curent_time = pygame.time.get_ticks()
            if curent_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):  # Ajusta al jugador a los limites de la pantalla
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint            
    
    def handle_vertical_collision(self, floor_rect, ladder_rects, dy):
        player_rect = self.rect
        
        if player_rect.colliderect(floor_rect):
            if dy > 0 and not self.on_ladder:
                self.rect.bottom = floor_rect.top
                self.landed()
                self.on_ground = True

            #elif dy < 0:
            #    self.rect.top = floor_rect.bottom
                #self.hit_head()
        else:
            self.rect.y += dy

        for ladder_rect in ladder_rects:
            if player_rect.colliderect(ladder_rect):
                #self.rect.x = ladder_rect.x
                self.on_ladder = True
                if not self.on_ladder:
                    self.rect.y += dy
                return True

    def handle_move(self):
        keys = pygame.key.get_pressed()
        self.is_moving = (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])
        self.x_vel = 0
        self.y_speed = 0

        if self.on_ground:
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.sound_steps.play()
            else:
                self.sound_steps.stop()
                self.move_pressed = False

            if keys[pygame.K_LEFT]:
                self.move_pressed = True
                self.move_left(self.speed)
            elif keys[pygame.K_RIGHT]:
                self.move_pressed = True
                self.move_right(self.speed)
            if not self.on_ladder:
                if keys[pygame.K_SPACE] and not self.space_pressed and self.jump_count < 2:
                    self.is_jumping = True
                    self.jump()
                if keys[pygame.K_LCTRL] and not self.space_pressed:
                    self.shoot()   
        
        if self.on_ladder:
            if keys[pygame.K_UP]:
                if not self.up_pressed:
                    self.chanel_ladder.play(self.sound_ladder)
                self.up_pressed = True
                self.move_up(self.speed_ladder)
            elif keys[pygame.K_DOWN]:
                if not self.up_pressed:
                    self.chanel_ladder.play(self.sound_ladder)
                self.up_pressed = True
                self.move_down(self.speed_ladder)

            else:
                self.chanel_ladder.stop()
                self.up_pressed = False
                 
        if not keys[pygame.K_LCTRL] and not keys[pygame.K_SPACE]:
            self.space_pressed = False  
        
        if not self.on_ladder:
            self.y_speed += min(1, (self.fall_count / FPS) * self.gravity)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        
        if self.direction != "left":
            self.direction = "left"
            self.animacion_contador = 0
        if not self.is_jumping:
            self.animacion_contador =  (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)
            self.image = pygame.transform.flip(self.move_images[self.animacion_contador // self.animation_speed_move], True, False)

    def move_right(self, vel):
        self.x_vel = vel
        
        if self.direction != "right":
            self.direction = "right"
            self.animacion_contador = 0
        if not self.is_jumping:
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)
            self.image = self.move_images[self.animacion_contador // self.animation_speed_move]

    def move_up(self, vel):
        self.y_speed = -vel
        #self.rect.y += self.y_speed

        if self.direction != "up":
            self.direction = "up"
            self.animacion_contador = 0
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_up)
        self.image = self.up_images[self.animacion_contador // self.animation_speed_up]

    def move_down(self, vel):
        self.y_speed = vel
        #self.rect.y += self.y_speed
        
        if self.direction != "down":
            self.direction = "down"
            self.animacion_contador = 0
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_up)
        self.image = self.up_images[self.animacion_contador // self.animation_speed_up]

    def idle(self):
        if not self.is_moving and self.ready and not self.is_jumping:
            if self.direction == "right":
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = self.idle_images[self.animacion_contador // self.animation_speed_idle]
            if self.direction == "left":
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = pygame.transform.flip(self.idle_images[self.animacion_contador // self.animation_speed_idle], True, False)
    
    def jump(self):
        if self.direction == "left":
            self.image = pygame.transform.flip(self.jump_images[0], True, False)   
        elif self.direction != "left":
            self.image = self.jump_images[0]

        self.y_speed = -self.gravity * self.speed_jump
        #self.animacion_contador = 0
        self.jump_count += 1

        if self.jump_count == 1:
            self.fall_count = 0

    def landed(self):
        self.fall_count = 0
        self.y_speed = 0
        self.jump_count = 0
        self.is_jumping = False 

    def hit_head(self):
        self.count = 0
        self.y_speed *= -1

    def shoot(self):
        #ANIMACION
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
        if self.direction == "right":
            self.image = self.fire_images[self.animacion_contador // self.animation_speed_fire]                
        elif self.direction == "left":
            self.image = pygame.transform.flip(self.fire_images[self.animacion_contador // self.animation_speed_fire], True, False)
        
        if self.municion > 0:
            # SONIDO          
            self.chanel_gun.play(self.sound_gun)
            self.shoot_laser()
        else:
            self.chanel_gun.play(self.sound_gun_empty)
        self.space_pressed = True
        self.ready = False
        self.laser_time = pygame.time.get_ticks()      


    def steps(self):
        if self.move_pressed:
            self.chanel_steps.play(self.sound_steps, -1)
        else:
            self.chanel_steps.stop()

    def do_dead(self):
        if self.animacion_contador == len(self.dead_images)-1:
            if self.direction == 'right':
                self.image = self.dead_images[-1]   
            else: 
                self.image = pygame.transform.flip(self.dead_images[-1], True, False)
            self.image.set_colorkey(WHITE)     
            if self.scream:
                self.chanel_dead.play(self.sound_dead)
                self.scream = False
        else:
            if self.animacion_contador < len(self.dead_images) * self.animation_dead:
                self.image = self.dead_images[self.animacion_contador // self.animation_dead]
                if not self.move_right:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.image.set_colorkey(WHITE)
                self.animacion_contador += 1
            else:
                self.animacion_contador = 0


    def update(self, screen: pygame.surface.Surface, pause):
        if self.is_dead:
            self.do_dead()
        elif pause:
            pass
        else:
            if not self.on_ladder:
                self.y_speed += min(1, (self.fall_count / FPS) * self.gravity)
            self.recharge()
            self.bullet_group.draw(screen)
            self.bullet_group.update()
            self.fall_count += 1
            self.handle_move()
            self.move(self.x_vel, self.y_speed)  
            self.idle()
            self.constraint()
            self.steps()
