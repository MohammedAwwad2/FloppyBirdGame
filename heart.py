import pygame


class heart:
    def __init__(self, screen, x, y):
        # super(lives, self).__init__()
        self.image = pygame.image.load("images/heart pixel art 254x254.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.screen = screen
        self.x = x
        self.y = y
        self.image_rect = self.image.get_rect()
        self.image_rect.y = self.y
        self.image_rect.x = self.x

    def update(self):
        self.screen.blit(self.image, self.image_rect)
