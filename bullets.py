import pygame
from pygame.sprite import Sprite


class Bullets(Sprite):
    def __init__(self, screen, Airplane):
        super(Bullets, self).__init__()

        self.screen = screen
        # ------load bullet  image and update its scale and rotate it (check #bullet image) in "images" folder)---------
        self.image = pygame.image.load("images/2-23861_bullet-transparent-flame-bullet-fire-png.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.image = pygame.transform.rotate(self.image, 45)
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------set position of bullets---------------------------------------
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.right = Airplane.rect.right
        self.rect.x = Airplane.rect.x + 60
        self.rect.centery = Airplane.rect.centery + 3
        # -----------------------------------------------------------------------------------------
        self.x = float(Airplane.rect.x + 60)
        self.bullet_speed = 3

    def draw(self):  # draw bullets
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.bullet_speed
        self.rect.x = self.x
