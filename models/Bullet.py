import pygame
from auxiliar.constantes import screen_w

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, img_path = False):
        super().__init__()
        self.__load_img(img_path)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction

    def __load_img(self, img_path: bool):
        if img_path:
            image_bullet = pygame.image.load('./assets/graphics/player_laser.png').convert_alpha()
            self.image = pygame.transform.scale(image_bullet, (20, 5))
        else: 
            self.image = pygame.Surface((1, 4))
            self.image.fill('white')

    def update(self):
        match self.direction:
            case 'right':
                self.rect.x += 50
                if self.rect.x >= screen_w:
                    self.kill()
            case 'left':
                self.rect.x -= 50
                if self.rect.x <= 0:
                    self.kill()