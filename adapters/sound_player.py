import pygame
from pygame.locals import *

class SoundPlayer:
    # Initialiserer pygame mixer for lydavspilling
    def __init__(self):
        pygame.mixer.init()

    # Laster og spiller av en lydfil
    def play_sound(self, sound_file):
        pygame.mixer.music.load(f"{sound_file}.mp3")
        pygame.mixer.music.play()

    # Stopper og fjerner lyden som spilles av
    def stop_sound(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    # Setter volumet til lyden som spilles av (0.0 til 1.0)
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

