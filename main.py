import random
from Classes import Powerup
from Classes import Floor
from Classes import MainCharacter
from Classes import Cloud
from Classes import Music
import pygame
import time
import requests
from pygame.locals import *

class ClassController():

    def __init__(self):
        """
        Initializing the basic parts of the game, such as the Music, MainCharacter, and Floor modules, the display, etc.
        """
        pygame.init()
        pygame.font.init()
        smallfont = pygame.font.SysFont('Arial', 22)
        largefont = pygame.font.SysFont('Arial', 30)
        pygame.mixer.init()
        pygame.display.set_caption("Parkour Simulator 2017")
        clock = pygame.time.Clock()

        self.music = Music.Music()

        self.screen_width = 640
        self.screen_height = 480
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])

        self.runnerboy = MainCharacter.MainCharacter((50, 249))

        self.currentscreen = "mainmenu"

        self.randomfloory = 300
        self.randomwidth = 200

        """
        Initialize all 4 floors at varying heights
        """
        self.floors = [Floor.Floor((50, self.randomfloory), self.randomwidth)]
        for i in range(3):
            self.randomfloory += random.randint(-50, 50)
            self.floors.append(Floor.Floor((300 + 250 * i, self.randomfloory), self.randomwidth))

        self.powerups = []
        self.powerupscooldown = 0
        cloudcooldown = random.randint(90, 200)

        self.clouds = [Cloud.Cloud()]

        self.score = 0


        loop = True
        while loop:
            """
            Check all input and see if player jumps, groundpounds, mutes the game, or tries to change screens
            """
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.currentscreen == "mainmenu":
                        self.currentscreen = "game"
                    elif event.key == pygame.K_SPACE and self.currentscreen == "deathscreen":
                        self.currentscreen = "game"
                    elif event.key == pygame.K_ESCAPE and self.currentscreen == "game":
                        self.currentscreen = "paused"
                    elif self.currentscreen == "paused" and (event.key == pygame.K_c or event.key == pygame.K_ESCAPE):
                        self.currentscreen = "game"
                    elif self.currentscreen == "paused" and event.key == pygame.K_q:
                        loop = False
                    elif event.key == pygame.K_m:
                        self.music.mute()
                    elif event.key == pygame.K_UP:
                        self.runnerboy.jump()
                    elif event.key == pygame.K_DOWN:
                        self.runnerboy.groundpound()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        if self.powerupscooldown > 0:
                            self.runnerboy.gravitymultiplier = 0.5
                        else:
                            self.runnerboy.gravitymultiplier = 1
                        self.runnerboy.maxyspeed = 6
                if event.type == pygame.QUIT:
                    loop = False

            """
            Show the correct screen and only run the code relating to the current screen.
            Make floors scroll infinitely, with a floor respawning on the right side of the screen
            if it disappears to the left. Spawn powerups randomly.
            """
            if self.currentscreen == "mainmenu":
                self.screen.fill((204,229,255))
                titletext = largefont.render(('Parkour Simulator 2017'), True, (0, 0, 0))
                self.screen.blit(titletext, (220, 100))


                pillimage = pygame.image.load('sprites/gravity.png').convert_alpha()
                chairimage = pygame.image.load('sprites/chair.png').convert_alpha()
                chairtext = smallfont.render(('Slows player on contact.'), True, (0,0,0))
                pilltext = smallfont.render(('Lowers the gravity of the player'), True, (0,0,0))
                highscoretext = smallfont.render((str(('High Score: ' + (open("highscore.txt", "r").readline())))), True, (0,0,0))
                tutorialtext = smallfont.render('Up on keyboard to jump, Down on keyboard to go down', True, (0,0,0))
                starttext = largefont.render('Press SPACE to start', True, (255,153,51))
                deathtext1 = largefont.render('YOU DIED', True, (0,0,0))
                deathtext2 = largefont.render('Press SPACE to restart', True, (0,0,0))

                self.screen.blit(pillimage, (200, 190))
                self.screen.blit(pilltext, (250, 200) )
                self.screen.blit(chairimage, (205, 230))
                self.screen.blit(chairtext, (250, 250))
                self.screen.blit(highscoretext, (275, 350))
                self.screen.blit(tutorialtext, (150, 160))
                self.screen.blit(starttext, (220, 400))

            elif self.currentscreen == "paused":
                self.screen.fill((204,229,255))
                paused_text = largefont.render('Game paused, press C to continue or Q to quit', True, (0,0,0))
                self.screen.blit(paused_text, (100,100))

            elif self.currentscreen == "deathscreen":
                highscoretext = smallfont.render((str(('High Score: ' + (open("highscore.txt", "r").readline())))), True, (0,0,0))
                self.screen.fill((178,34,34))
                self.screen.blit(deathtext1, (275,165))
                self.screen.blit(deathtext2, (220,280))
                self.screen.blit(quotetext, (quotex, 70))
                self.screen.blit(authortext, (authorx, 100))
                self.screen.blit(highscoretext, (265,350))

            else:
                for i in range(len(self.floors)):
                    if self.floors[i].x + self.floors[i].width < 0:
                        self.randomfloory += random.randint(-50, 50)
                        if self.randomfloory >= 420:
                            self.randomfloory = 420
                        elif self.randomfloory <= 60:
                            self.randomfloory = 60
                        randomwidth = random.randint(150,350)
                        if i == 0:
                            self.floors[i] = Floor.Floor((self.floors[len(self.floors)-1].x + self.floors[i - 1].width + 50, self.randomfloory), randomwidth)
                        else:
                            self.floors[i] = Floor.Floor((self.floors[i - 1].x + self.floors[i - 1].width + 50, self.randomfloory), randomwidth)
                        if random.randint(0,2) == 1:
                            self.powerups.append(Powerup.Powerup((self.floors[i].x + self.floors[i].width / 2 - 31, self.randomfloory - 43)))

                self.screen.fill((254,91,53))

                """
                Check whether the powerup has faded and whether it's time to spawn a new cloud, and update clouds.
                """

                if self.powerupscooldown > 0:
                    self.powerupscooldown -= 1
                    if self.powerupscooldown <= 0:
                        self.runnerboy.gravitymultiplier = 1

                if cloudcooldown <= 0:
                    self.clouds.append(Cloud.Cloud())
                    cloudcooldown = random.randint(90,200)
                else:
                    cloudcooldown -= 1

                for i in range(len(self.clouds)):
                    self.clouds[i].always()
                    self.screen.blit(self.clouds[i].image, (self.clouds[i].x, self.clouds[i].y))
                    if self.clouds[i].x > 660 or self.clouds[i].x < -60:
                        del self.clouds[i]
                        if len(self.clouds) > 0:
                            for j in range(i, len(self.clouds)):
                                self.clouds[j].always()
                                self.screen.blit(self.clouds[j].image, (self.clouds[j].x, self.clouds[j].y))
                        break


                """
                Update floors/buildings and powerups.
                Check for collisions between the powerups and player and apply the consequences.
                """


                for i in range(len(self.floors)):
                    self.floors[i].always(self.runnerboy.speed)
                    self.screen.blit(self.floors[i].image, (self.floors[i].x, self.floors[i].y))

                for i in range(len(self.powerups)):
                    self.powerups[i].always(self.runnerboy.speed)
                    self.screen.blit(self.powerups[i].image, (self.powerups[i].x, self.powerups[i].y))
                    if pygame.sprite.collide_rect(self.runnerboy, self.powerups[i]):
                        if self.powerups[i].type == "chair":
                            self.runnerboy.speed -= 1
                            del self.powerups[i]
                        elif self.powerups[i].type == "gravity":
                            self.runnerboy.gravitymultiplier = 0.5
                            del self.powerups[i]
                            self.powerupscooldown = 150
                        if len(self.powerups) > 0:
                            for j in range(i, len(self.powerups)):
                                self.powerups[j].always(self.runnerboy.speed)
                                self.screen.blit(self.powerups[j].image, (self.powerups[j].x, self.powerups[j].y))
                        break
                    if self.powerups[i].x + 62 < 0:
                        del self.powerups[i]
                        if len(self.powerups) > 0:
                            for i in range(i, len(self.powerups)):
                                self.powerups[i].always(self.runnerboy.speed)
                                self.screen.blit(self.powerups[i].image, (self.powerups[i].x, self.powerups[i].y))
                        break

                """
                Update player and score and check for death, then prepare and set the death screen.
                Show score and, if applicable, powerup cooldown text.
                """

                self.runnerboy.always(self.floors,self.powerups)
                self.screen.blit(self.runnerboy.image, (self.runnerboy.x, self.runnerboy.y))

                if self.runnerboy.y > 480:

                    if self.score > int((open("highscore.txt", "r").readline())):
                        (open("highscore.txt", "w").write(str(self.score)))
                    self.reset()
                    try:
                        quotes = requests.get('https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json')
                        currquote = quotes.json()
                        if len(currquote["quoteText"]) < 80:
                            quotetext = smallfont.render(('"' + currquote["quoteText"] + '"'), True, (0,0,0))
                            authortext = smallfont.render(('-' + currquote["quoteAuthor"]), True, (0,0,0))
                            quotex = (self.screen_width - smallfont.size(currquote["quoteText"])[0]) / 2
                            authorx = (self.screen_width - smallfont.size(currquote["quoteAuthor"])[0]) / 2
                        else:
                            quotetext = smallfont.render('"How do I keep on losing at poker?"', True, (0,0,0))
                            authortext = smallfont.render("-Colin", True, (0,0,0))
                            quotex = 200
                            authorx = 300

                    except:
                        quotetext = smallfont.render('"How do I keep on losing at poker?"', True, (0,0,0))
                        authortext = smallfont.render("-Colin", True, (0,0,0))
                        quotex = 200
                        authorx = 300

                    self.currentscreen = "deathscreen"
                if not self.runnerboy.dead:
                    self.score += int(self.runnerboy.speed // 4)

                self.scoretext = smallfont.render((str(('Score: ' + str(self.score)))), True, (0,0,0))
                self.screen.blit(self.scoretext, (10, 10))

                if self.powerupscooldown > 0:
                    self.screen.blit(smallfont.render(('Gravity: ' + str(self.powerupscooldown)), True, (0,0,0)), (10, 25))

            pygame.display.update()
            clock.tick(60)

    def reset(self):
        """
        Reset everything, both variables and objects.
        """
        self.cloudcooldown = random.randint(90,200)
        self.clouds = [Cloud.Cloud()]
        self.runnerboy.reset((50, 249))
        self.randomfloory = 300
        for i in range(len(self.floors)):
            if i > 0:
                self.randomfloory += random.randint(-50, 50)
            self.floors[i].reset(i, self.randomfloory)
        self.powerups = []
        self.powerupscooldown = 0
        self.score = 0


main = ClassController()