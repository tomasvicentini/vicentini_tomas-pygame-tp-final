import pygame
from models.Bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, stage_dict_configs: dict):
        super().__init__()

        self.__player_configs = stage_dict_configs.get('player')
        # Sprite del jugador movimiento
        self.move_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs["run_img"]]

        # Sprite del jugador iddle
        self.idle_images = [pygame.image.load(image).convert_alpha() for image in self.__player_configs["idle_img"]]

        # Establecer la imagen actual
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.original_image = self.image

        # Atributos de movimiento
        self.speed = self.__player_configs["speed"]
        self.max_x_constraint = constraint

        # Atributos para disparar y recargar
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.bullet_group = pygame.sprite.Group()
        self.puntaje = 0
        self.is_moving = False
        self.animacion_contador = 0

    def manejar_eventos_teclado(self):  # Eventos del jugador
        """
        The function handles keyboard events for player movement and shooting lasers.
        """
        keys = pygame.key.get_pressed()
        
        is_moving_previous = self.is_moving
        self.is_moving = keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]

        if self.is_moving:
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.move_images) * 5)

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.move_images[self.animacion_contador // 5]
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.move_images[self.animacion_contador // 5], True, False)
        else:
            # No se está moviendo
            self.animacion_contador = (self.animacion_contador + 1) % (len(self.idle_images) * 30)
            self.image = self.idle_images[self.animacion_contador // 30]
            
            if not is_moving_previous:
                # Si no se estaba moviendo antes, ajustar la imagen para que mire en la dirección correcta
                self.image = pygame.transform.flip(self.image, keys[pygame.K_LEFT], False)

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    @property
    def get_bullets(self) -> list[Bullet]:
        return self.bullet_group
    
    def shoot_laser(self):  # disparar laser
        print('!piu piu!')
        print(f"{self.speed}")
        self.bullet_group.add(self.create_bullet())

    def create_bullet(self):
        direction = 'right' if self.speed > 0 else 'left'
        return Bullet(self.rect.centerx, self.rect.top, direction, True)
        
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
