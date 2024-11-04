import pygame
from pygame.locals import *

pygame.mixer.init()

def playSound(soundFile):
    pygame.mixer.music.load(soundFile)
    pygame.mixer.music.play()

def stopSound():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

def setVolume(volume):
    pygame.mixer.music.set_volume(volume)
