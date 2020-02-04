import random
import pygame
from pygame.locals import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, pos, width):
        """
        Initialize the floor with the width and position provided.
        Randomly choose color and initialize rect.
        """

        self.width = width
        self.image = pygame.Surface((self.width,500))
        self.image.fill((random.choice([(0,0,0), (50,50,50), (32,32,32)])))
        self.x = pos[0]
        self.y = pos[1]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


    def always(self, speed):
        """
        Update coordinates.
        """
        self.x -= speed
        self.rect.topleft = (self.x, self.y)

    def reset(self, floornum, y):
        """
        Reset the coordinates depending on which building it is assigned to be, and
        reset variables and randomly set color.
        """
        if floornum == 0:
            self.x = 50
        elif floornum == 1:
            self.x = 300
        elif floornum == 2:
            self.x = 550
        elif floornum == 3:
            self.x = 800
        self.width = 200
        self.y = y
        self.image = pygame.Surface((self.width,500))
        self.image.fill((random.choice([(0, 0, 0), (50, 50, 50), (32, 32, 32)])))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
