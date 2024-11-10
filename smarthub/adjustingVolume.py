import pygame
from pygame.locals import *

class SoundPlayer:
    def __init__(self): """Initialize the pygame mixer for audio playback."""
        pygame.mixer.init()

    def play_sound(self, sound_file):   """Load and play a sound file."""
        pygame.mixer.music.load(f"{sound_file}.mp3")
        pygame.mixer.music.play()

    def stop_sound(self):   """Stop and unload the current sound."""
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def set_volume(self, volume):   """Set the playback volume (0.0 to 1.0)."""
        pygame.mixer.music.set_volume(volume)