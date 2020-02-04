import pygame
from pygame.locals import *

class Music():
    def __init__(self):
        """
        Load the music, play it, and set it to 60% volume.
        """
        pygame.mixer.music.load("audio/music.mp3")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.6)

    def mute(self):
        """
        Mute or unmute the music, depending on whether it's already muted or not.
        """
        if pygame.mixer.music.get_volume() == 0.0:
            pygame.mixer.music.set_volume(0.6)
        else:
            pygame.mixer.music.set_volume(0.0)

