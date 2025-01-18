import pygame
from pygame import mixer


class airplane(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(airplane, self).__init__()
        # -------------------- starting position of airplane----------------------
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.x = 30
        self.y = (self.screen_rect.height // 2) - 50
        # --------------------------------------------------------------------------
        # --------load airplane images and  change their width and height--------
        self.airplane_images = []
        self.append_images()
        # --------------------------------------------------------------------------
        self.index = 0  # index of one of airplane's images
        self.lives = 3  # number of lives
        self.score = 0
        self.angel = 0  # angel of airplane
        self.image = None
        self.rect = None
        # ------------- ----------- some flags for keys----------------------------
        self.Up = False
        self.Down = False
        # ------------------------------------------------------------------------
        self.gain_heal_sound = mixer.Sound("audio/healpop-46004.mp3")
        self.i = 1

    def append_images(
            self):  # this function append images of airplane to "append_images" list and change their width and height
        for i in range(1, 5):
            airplane_image = pygame.image.load(f"images/air{i}.png")
            airplane_image = pygame.transform.scale(airplane_image, (90, 90))
            self.airplane_images.append(airplane_image)

    def update(self, birds_Group):
        self.index += 1
        if self.index >= len(self.airplane_images):
            self.index = 0
        self.image = self.airplane_images[self.index]
        self.rect = self.image.get_rect()

        self.image = pygame.transform.rotate(self.image, self.angel)

        self.rect.x = self.x
        self.rect.y = self.y

        if pygame.sprite.spritecollide(self, birds_Group, True):
            self.lives -= 1
        if self.score % 20 == 0:
            if self.lives < 3:
                self.lives = 3
                self.gain_heal_sound.play()

    def update_key(self):  # check keys and update angel
        if self.Up and self.rect.top >= 20:
            self.y -= 4
            self.angel = 15
        elif self.Down and self.rect.bottom <= self.screen_rect.height - 30:
            self.y += 4
            self.angel = -15
        else:
            self.angel = 0
