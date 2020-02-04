import pygame
from pygame.locals import *
from Classes import Powerup
from Classes import Floor
from Classes import MainCharacter
from Classes import Cloud
from Classes import Music


def main():

    screen = pygame.display.set_mode([640,480])

    pygame.mixer.init()


    print('=========Test Character=========')
    test_character = MainCharacter.MainCharacter((0,0))
    test_character.onGround = True

    print('=========Positive Vertical Movement==========')
    test_character.jump()
    if test_character.onGround:
        assert test_character.y == -13

    print('=========Ground Pound Test==========')
    test_character.groundpound()
    assert test_character.gravitymultiplier == 5

    print('=========Powerup Test=========')
    test_powerup = Powerup.Powerup((0,0))
    assert test_powerup.type == "chair" or test_powerup.type == "gravity"

    print('=========Cloud Test=========')
    test_cloud = Cloud.Cloud()
    assert test_cloud.x == -60 or test_cloud.x == 660

    print('=========Floor Test=========')
    test_floor = Floor.Floor((50,10),150)
    assert test_floor.x == 50
    assert test_floor.y == 10
    assert test_floor.width == 150

    print('=========Music Test=========')
    test_music = Music.Music()
    test_music.mute()
    assert pygame.mixer.music.get_volume() == 0.0

main()