import pygame
import os
from SQ_modules.configs import GAME_VOLUME
import random
import time

def fade_out_sound(sound: pygame.mixer.Sound, fade_duration_ms: int):
    original_volume = sound.get_volume()
    steps = 20
    sleep_time = fade_duration_ms / (steps * 1000.0)
    
    for step in range(steps, 0, -1):
        new_volume = original_volume * (step / steps)
        sound.set_volume(new_volume)
        time.sleep(sleep_time)
    
    sound.stop()
    sound.set_volume(original_volume)

class GameAudio:
    def __init__(self):

        slide_sounds_dir = "resources/audio/sounds/SlideSounds"
        self.slide_sfxs: list[pygame.mixer.Sound] = []
        for sound_file in os.listdir(slide_sounds_dir):
            sfx = pygame.mixer.Sound(os.path.join(slide_sounds_dir, sound_file))
            sfx.set_volume(GAME_VOLUME)
            self.slide_sfxs.append(sfx)


        self.level_complete_sfx = pygame.mixer.Sound("resources/audio/sounds/LevelCompleteSound.mp3")
        self.level_complete_sfx.set_volume(GAME_VOLUME)
        self.title_screen_music = pygame.mixer.Sound("resources/audio/music/PhilosophicalSongTitle - RoccoW  Chiptune [No Copyright Music].mp3")
        self.title_screen_music.set_volume(GAME_VOLUME)

    def PlayRandomSlideSfx(self):
        """
        Plays a random sliding sound effect.
        """
        sfx = random.choice(self.slide_sfxs)
        sfx.play()
    
    def FadeOutMusic(self, fade_duration_ms: int = 3000):
        fade_out_sound(self.title_screen_music, fade_duration_ms)