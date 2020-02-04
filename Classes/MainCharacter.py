
import pygame
from pygame.locals import *

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, pos):
        """
        Initialize all main character variables, such as the gravity, maxspeed, and its coordinates and image.
        Load images.
        """

        self.gravity = 0.9
        self.gravitymultiplier = 1
        self.speed = 6
        self.maxspeed = 12
        self.yspeed = 1
        self.maxyspeed = 6
        self.x = pos[0]
        self.y = pos[1]
        self.dead = False
        self.image = pygame.image.load('sprites/player/run/run1.gif').convert_alpha()
        self.currentanim = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.jumpforce = -11
        self.animcooldown = 1.5
        self.onGround = False
        self.runanims = [pygame.image.load('sprites/player/run/run1.gif').convert_alpha(), pygame.image.load('sprites/player/run/run2.gif').convert_alpha(), pygame.image.load('sprites/player/run/run3.gif').convert_alpha(), pygame.image.load('sprites/player/run/run4.gif').convert_alpha(), pygame.image.load('sprites/player/run/run5.gif').convert_alpha(), pygame.image.load('sprites/player/run/run6.gif').convert_alpha(), pygame.image.load('sprites/player/run/run7.gif').convert_alpha(), pygame.image.load('sprites/player/run/run8.gif').convert_alpha()]
        self.jumpanim = pygame.image.load('sprites/player/jump.gif').convert_alpha()

    def always(self, buildings, powerups):
        """
        Check whether it's colliding with the buildings and whether it's hitting the side or rooftop, and apply the
        correct consequences.
        Update its coordinates, speed, and animation.
        """

        self.onGround = False
        for i in range(len(buildings)):
            if pygame.sprite.collide_rect(self, buildings[i]):
                if self.y + 37 > buildings[i].y:
                    self.speed = -0.3
                    self.yspeed = 14
                    self.dead = True
                else:
                    self.onGround = True
                    self.yspeed = 0
                break

        if self.yspeed < self.maxyspeed and not self.onGround:
            self.yspeed += self.gravity * self.gravitymultiplier
        self.y += self.yspeed
        self.animcooldown -= 1
        if self.animcooldown < 0:
            if self.onGround == True:
                if self.currentanim == len(self.runanims) - 1:
                    self.currentanim = 0
                else:
                    self.currentanim += 1
                self.image = self.runanims[self.currentanim]
            self.animcooldown = 1.5
        if self.speed < self.maxspeed:
                self.speed *= 1.001
        self.rect.topleft = (self.x, self.y)




    def jump(self):
        """
        Jump and set the yspeed which dictates the force. Updates coordinates.
        """
        if self.onGround:
            self.currentanim = 0
            self.image = self.jumpanim
            self.y -= 13
            self.yspeed = self.jumpforce
            self.onGround = False
            self.rect.topleft = (self.x, self.y)

    def groundpound(self):
        """
        Update variables to quickly accelerate negatively.
        """
        self.maxyspeed = 7
        self.gravitymultiplier = 5

    def reset(self, pos):
        """
        Reset all important variables.
        """
        self.gravity = 0.9
        self.gravitymultiplier = 1
        self.speed = 6
        self.maxspeed = 12
        self.yspeed = 1
        self.maxyspeed = 6
        self.x = pos[0]
        self.y = pos[1]
        self.dead = False
        self.rect.topleft = (self.x, self.y)
