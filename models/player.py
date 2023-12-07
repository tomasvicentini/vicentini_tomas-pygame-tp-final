import pygame
from models.Bullet import Bullet
from auxiliar.constantes import (FPS)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, stage_dict_configs: dict):
        super().__init__()
        self.__player_configs = stage_dict_configs.get('player')
        
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['run_img']] # Sprite player run
        self.idle_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['idle_img']] # Sprite player iddle
        self.fire_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['fire_img']] # Sprite player fire
        self.jump_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['jump_img']] # Sprite player jump
        self.up_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['up_img']] # Sprite player up

        # Establecer la imagen actual
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.original_image = self.image
 
        # Atributos de movimiento
        self.speed = self.__player_configs['speed']
        
        self.max_x_constraint = constraint
        
        #NUEVOS METODOS
        self.direction = "right"
        #self.animation_count = 0
        self.x_vel = 0
        self.y_speed = 0
        self.is_moving = False
        self.animacion_contador = 0
        self.animation_speed_idle = 30
        self.animation_speed_fire = 15
        self.animation_speed_move = 5
        self.animation_speed_jump = 5

        # GRAVEDAD - SALTO
        self.fall_count = 0
        self.gravity = 1
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

        
        self.space_pressed = False

        # Pisos
        self.on_floor = False
        self.floor_class = []

        # Escaleras
        self.on_ladder = False
        self.lock_ladder = False



    @property
    def get_bullets(self) -> list[Bullet]:
        return self.bullet_group
    
    def shoot_laser(self):  # disparar laser
        self.bullet_group.add(self.create_bullet())

    def create_bullet(self):
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
            if dy > 0:
                self.rect.bottom = floor_rect.top
                self.landed()
            elif dy < 0:
                self.rect.top = floor_rect.bottom
                self.hit_head()
        else:
            self.rect.y += dy

        for ladder_rect in ladder_rects:
            if player_rect.colliderect(ladder_rect):
                # Ajustar la posición horizontal del jugador en la escalera
                self.rect.x = ladder_rect.x

                if not self.on_ladder:
                    # Si no está en una escalera, ajustar la posición vertical
                    self.rect.y += dy
                return True

    def handle_move(self):
        keys = pygame.key.get_pressed()
        self.is_moving = (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT])
        self.x_vel = 0
        self.y_speed = 0

        if self.on_ladder:
            if keys[pygame.K_UP]:
                self.move_up(self.speed_ladder)
            if keys[pygame.K_DOWN]:
                self.move_down(self.speed_ladder)
        else:
            if keys[pygame.K_LEFT]:
                self.move_left(self.speed)
            if keys[pygame.K_RIGHT]:
                self.move_right(self.speed)
            if keys[pygame.K_SPACE] and not self.space_pressed and self.jump_count < 2:
                self.is_jumping = True
                self.jump()
            if keys[pygame.K_LCTRL] and not self.space_pressed:
                self.shoot()   
                 
        if not keys[pygame.K_LCTRL] or not keys[pygame.K_SPACE]:
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
        self.animacion_contador =  (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)
        self.image = pygame.transform.flip(self.move_images[self.animacion_contador // self.animation_speed_move], True, False)

    def move_right(self, vel):
        self.x_vel = vel
        
        if self.direction != "right":
            self.direction = "right"
            self.animacion_contador = 0
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)
        self.image = self.move_images[self.animacion_contador // self.animation_speed_move]

    def move_up(self, vel):
        self.y_speed = -vel
        #self.rect.y += self.y_speed

        if self.direction != "up":
            self.direction = "up"
            self.animacion_contador = 0
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_move)
        self.image = self.up_images[self.animacion_contador // self.animation_speed_move]


    def move_down(self, vel):
        self.y_speed = vel
        #self.rect.y += self.y_speed
        
        if self.direction != "down":
            self.direction = "down"
            self.animacion_contador = 0
        self.animacion_contador = (self.animacion_contador + 1) % (len(self.up_images) * self.animation_speed_move)
        self.image = self.up_images[self.animacion_contador // self.animation_speed_move]

    def idle(self):
        if not self.is_moving and self.ready:
            if self.direction == "right":
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = self.idle_images[self.animacion_contador // self.animation_speed_idle]
            if self.direction == "left":
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = pygame.transform.flip(self.idle_images[self.animacion_contador // self.animation_speed_idle], True, False)
    
    def jump(self):
        self.y_speed = -self.gravity * self.speed_jump
        self.animacion_contador = 0
        self.jump_count += 1

        if self.jump_count == 1:
            self.fall_count = 0
        if self.direction == "right":
            self.image = self.jump_images[0]
        if self.direction == "left":
            self.image = pygame.transform.flip(self.jump_images[0], True, False)         



        print(f"jump_count:{self.jump_count} | fall_count:{self.fall_count} | y_speed: {self.y_speed}| gravity: {self.gravity}") 

    def landed(self):
        self.fall_count = 0
        self.y_speed = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_speed *= -1

    def shoot(self):
        if self.direction == "right":
            self.shoot_laser()
            self.space_pressed = True
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
            self.image = self.fire_images[self.animacion_contador // self.animation_speed_fire]                
        if self.direction == "left":
            self.shoot_laser()
            self.space_pressed = True
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
            self.image = pygame.transform.flip(self.fire_images[self.animacion_contador // self.animation_speed_fire], True, False)   

    def update(self, screen: pygame.surface.Surface):
        if not self.on_ladder:
            self.y_speed += min(1, (self.fall_count / FPS) * self.gravity)
        self.handle_move()
        self.move(self.x_vel, self.y_speed)  
        self.idle()
        self.constraint()
        self.recharge()
        self.bullet_group.draw(screen)
        self.bullet_group.update()
        self.fall_count += 1