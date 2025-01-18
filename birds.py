import pygame
import random


class birds(pygame.sprite.Sprite):
    def __init__(self, screen, birds_images, birds_colors):
        super(birds, self).__init__()
        # ------------------ get screen rect----------- -----
        self.image = None
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.x = self.screen_rect.width
        self.y = random.randrange(50, self.screen_rect.height - 50)
        # -------------------index of bird_image-----------
        self.index = 0
        # -----------------choose random bird -------------
        self.bird_color = random.choice(birds_colors)
        self.bird = birds_images[self.bird_color]
        self.rect = self.bird[self.index].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        # -------------------------------------------------
        self.speed = 1

    def update(self, bullets_Group, airp, birds_images, bird_colors):
        # ------------------------update bird_image-------------------
        self.index += 1
        if self.index >= (len(birds_images[self.bird_color]) * 4):
            self.index = 0
        self.image = birds_images[self.bird_color][int(self.index // 4)]
        self.rect = self.image.get_rect()

        if airp.score % 30 >= 15:  # every 15 scores the birds will  increase their speed until player reach another  15
            # scores
            self.x -= 7 + self.speed
        else:
            self.x -= 5
            self.speed += 0.1
        self.rect.x = self.x
        self.rect.y = self.y
        # -----------------------check collide-------------------------
        self.check_collide(airp, bullets_Group)

    def check_collide(self, airp, bullets_Group):
        if pygame.sprite.spritecollide(self, bullets_Group, True):
            self.kill()
            airp.score += 1
        if self.x < 0:
            self.kill()
            airp.lives -= 1

    def check_x(self):
        return self.x
