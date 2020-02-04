import random
import pygame
from pygame.locals import *

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        """
        Initialize the image, speed, coordinates, and randomly choose direction.
        """
        self.image = pygame.image.load('sprites/cloud.png')
        self.rect = self.image.get_rect()
        self.speed = 1
        self.right = random.choice([True, False])
        if self.right:
            self.x = 660
        else:
            self.x = -60
        self.y = random.randint(0,270)

    def always(self):
        """
        Update x-coordinates.
        """
        if self.right:
            self.x -= self.speed
        else:
            self.x += self.speed
        self.rect.topleft = (self.x, self.y)