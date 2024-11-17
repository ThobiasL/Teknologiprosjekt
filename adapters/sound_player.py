import pygame
import os

class SoundPlayer:
    def __init__(self):
        self.root = os.path.dirname(os.path.asbath(__file__))
        self.audio_dir = os.path.join(self.root, 'audio')
        """Initialiser pygame mixer for lydavspilling."""
        pygame.mixer.init()
        self.current_sound = None
        self.is_playing = False
        self.paused_position = 0  # i sekunder
        self.last_time_rec = 0

        # Last inn alarmlyden separat
        try:
            self.alarm_sound = pygame.mixer.Sound("audio/alarm.mp3")
            self.go_for_a_walk_sound = pygame.mixer.Sound("audio/go_for_a_walk.mp3")
            self.eat_dinner_sound = pygame.mixer.Sound("audio/eat_dinner.mp3")
            print("Lyden lastet inn.")
        except pygame.error as e:
            print(f"Feil ved lasting av alarm.mp3: {e}")
            self.alarm_sound = None
            self.go_for_a_walk_sound = None
            self.eat_dinner_sound = None
        self.alarm_channel = None
        self.go_for_a_walk_channel = None
        self.eat_dinner_channel = None

    def play_sound(self, sound_file, start=0.0):
        """Last inn og spill av en lydfil ved bruk av pygame.mixer.music."""
        try:
            pygame.mixer.music.load(f"audio/{sound_file}.mp3")
            pygame.mixer.music.play(start=start)
            self.current_sound = sound_file
            self.is_playing = True
            self.paused_position = start
            print(f"Spiller av {sound_file}.mp3 fra {start} sekunder.")
        except pygame.error as e:
            print(f"Feil ved avspilling av {sound_file}.mp3: {e}")

    def stop_sound(self):
        """Stopp og tøm den nåværende musikken."""
        pygame.mixer.music.stop()
        self.current_sound = None
        self.is_playing = False
        self.paused_position = 0
        print("Stoppet musikk.")

    def set_volume(self, volume):
        """Sett avspillingsvolumet (0.0 til 1.0)."""
        pygame.mixer.music.set_volume(volume)

    def pause_sound(self):
        """Pausér den nåværende musikken ved å stoppe og lagre posisjonen."""
        if self.is_playing:
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms != -1:
                self.paused_position += pos_ms  / 1000.0  # konverter til sekunder
                self.last_time_rec = self.paused_position + 3
                print(f"Pauset musikk ved {self.paused_position} sekunder.")
            else:
                print("Kunne ikke hente posisjon ved pausing.")
            pygame.mixer.music.pause()
            self.is_playing = False

    def unpause_sound(self):
        """Gjenoppta den pauserte musikken ved å laste og spille fra posisjonen."""
        if self.current_sound is not None:
            try:
                #pygame.mixer.music.unload("audio/alarm.mp3")
               # pygame.mixer.music.load("audio/radio_simulering.mp3")
               # pygame.mixer.music.play(start=self.last_time_rec)
                pygame.mixer.music.unpause()
                self.is_playing = True
                print(f"Gjenopptatt musikk ved {self.paused_position} sekunder.")
            except pygame.error as e:
                print(f"Feil ved gjenopptakelse av {self.current_sound}.mp3: {e}")

    def sound_is_not_playing(self):
        """Returner True hvis ingen musikk spiller."""
        return not pygame.mixer.music.get_busy()

    def get_playing_position(self):
        """Returner nåværende avspillingsposisjon i millisekunder."""
        pos = pygame.mixer.music.get_pos()
        if pos != -1:
            total_pos = self.paused_position + (pos / 1000.0)  # konverter til sekunder
            print(f"Nåværende posisjon i musikk: {total_pos} sekunder.")
            return total_pos
        else:
            print("Kunne ikke hente posisjon.")
            return self.paused_position

    def play_alarm(self):
        """Spill av alarmlyden."""
        if self.alarm_sound:
            if self.alarm_channel is None or not self.alarm_channel.get_busy():
                self.alarm_channel = self.alarm_sound.play()
                print("Alarm lyden spilles av.")
            else:
                print("Alarm lyden spiller allerede.")

    def stop_alarm(self):
        """Stopp alarmlyden."""
        if self.alarm_channel:
            self.alarm_channel.stop()
            self.alarm_sound = None
            self.alarm_channel = None
            #pygame.mixer.sound.unload("audio/alarm.mp3")
            #self.alarm_channel.unload()
            #self.alarm_sound.unload()
            #pygame.mixer.Sound.unload()
            print("Alarm lyden stoppet.")

    def play_go_for_a_walk(self):
        """Spill av alarmlyden."""
        if self.go_for_a_walk_sound:
            if self.go_for_a_walk_channel is None or not self.go_for_a_walk_channel.get_busy():
                self.go_for_a_walk_channel = self.go_for_a_walk_sound.play()
                print("Alarm lyden spilles av.")
            else:
                print("Alarm lyden spiller allerede.")

    def stop_go_for_a_walk(self):
        """Stopp alarmlyden."""
        if self.go_for_a_walk_channel:
            self.go_for_a_walk_channel.stop()
            self.go_for_a_walk_sound = None
            self.go_for_a_walk_channel = None

    def play_eat_dinner(self):
        """Spill av alarmlyden."""
        if self.alarm_sound:
            if self.alarm_channel is None or not self.alarm_channel.get_busy():
                self.alarm_channel = self.alarm_sound.play()
                print("Alarm lyden spilles av.")
            else:
                print("Alarm lyden spiller allerede.")

    def stop_eat_dinner(self):
        """Stopp alarmlyden."""
        if self.eat_dinner_channel:
            self.eat_dinner_channel.stop()
            self.eat_dinner_sound = None
            self.eat_dinner_channel = None
