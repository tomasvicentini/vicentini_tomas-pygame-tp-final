import pygame
from models.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, stage_dict_configs: dict):
        super().__init__()

        self.__player_configs = stage_dict_configs.get('player')
        
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['run_img']] # Sprite player run
        self.idle_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['idle_img']] # Sprite player iddle
        self.fire_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs['fire_img']] # Sprite player fire

        # Establecer la imagen actual
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.original_image = self.image

        # Atributos de movimiento
        self.speed = self.__player_configs['speed']
        self.max_x_constraint = constraint
        self.move_right = True
        self.animation_speed_idle = 30
        self.animation_speed_fire = 15
        self.animation_speed_move = 5

        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.bullet_group = pygame.sprite.Group()
        self.puntaje = 0
        self.is_moving = False
        self.animacion_contador = 0
        self.space_pressed = False
        

    def manejar_eventos_teclado(self):  # Eventos del jugador
        keys = pygame.key.get_pressed()        
        is_moving_previous = self.is_moving
        self.is_moving = keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]

        if self.is_moving:
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * self.animation_speed_move)

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.move_images[self.animacion_contador // self.animation_speed_move]
            self.move_right = True
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.move_images[self.animacion_contador // self.animation_speed_move], True, False)
            self.move_right = False
        else:
            if self.move_right:
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = self.idle_images[self.animacion_contador // self.animation_speed_idle]
            else:
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * self.animation_speed_idle)
                self.image = pygame.transform.flip(self.idle_images[self.animacion_contador // self.animation_speed_idle], True, False)
            
            if not is_moving_previous:
                self.image = pygame.transform.flip(self.image, keys[pygame.K_LEFT], False)

        if keys[pygame.K_SPACE] and not self.space_pressed:
            self.shoot_laser()
            self.space_pressed = True
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            if self.move_right:
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
                self.image = self.fire_images[self.animacion_contador // self.animation_speed_fire]                
            else:
                self.animacion_contador = (self.animacion_contador + 1) % (len(self.fire_images) * self.animation_speed_fire)
                self.image = pygame.transform.flip(self.fire_images[self.animacion_contador // self.animation_speed_fire], True, False)    

        if not keys[pygame.K_SPACE]:
            self.space_pressed = False         

    @property
    def get_bullets(self) -> list[Bullet]:
        return self.bullet_group
    
    def shoot_laser(self):  # disparar laser
        self.bullet_group.add(self.create_bullet())

    def create_bullet(self):
        direction = 'right' if self.move_right else 'left'
        return Bullet(self.rect.centerx, self.rect.top+17, direction, True)
        
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

    def update(self, screen: pygame.surface.Surface):
        self.manejar_eventos_teclado()
        self.constraint()
        self.recharge()
        self.bullet_group.draw(screen)
        self.bullet_group.update()
