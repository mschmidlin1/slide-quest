import pygame
import os
from SQ_modules.configs import GAME_VOLUME
from SQ_modules.Metas import SingletonMeta
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

class GameAudio(metaclass=SingletonMeta):
    def __init__(self):
        pygame.mixer.init()
        self.volume = GAME_VOLUME
        slide_sounds_dir = "resources/audio/sounds/SlideSounds"
        self.slide_sfxs: list[pygame.mixer.Sound] = []
        for sound_file in os.listdir(slide_sounds_dir):
            sfx = pygame.mixer.Sound(os.path.join(slide_sounds_dir, sound_file))
            sfx.set_volume(self.volume)
            self.slide_sfxs.append(sfx)


        self.level_complete_sfx = pygame.mixer.Sound("resources/audio/sounds/LevelCompleteSound.mp3")
        self.level_complete_sfx.set_volume(self.volume)
        self.title_screen_music = pygame.mixer.Sound("resources/audio/music/PhilosophicalSongTitle - RoccoW  Chiptune [No Copyright Music].mp3")
        self.title_screen_music.set_volume(self.volume)
        self.button_click_sfx = pygame.mixer.Sound("resources/audio/sounds/multi-pop.mp3")
        self.button_click_sfx.set_volume(self.volume)
        self.splash_screen_sounds = pygame.mixer.Sound("resources/audio/sounds/vibes-windy-whoosh-magical-chimes.mp3")
        self.splash_screen_sounds.set_volume(self.volume)

    def PlayRandomSlideSfx(self):
        """
        Plays a random sliding sound effect.
        """
        sfx = random.choice(self.slide_sfxs)
        sfx.play()
    
    def FadeOutMusic(self, fade_duration_ms: int = 3000):
        fade_out_sound(self.title_screen_music, fade_duration_ms)
    
    def update_sfx_volume(self, volume: float):
        self.level_complete_sfx.set_volume(volume)
        for sfx in self.slide_sfxs:
            sfx.set_volume(volume)
        self.button_click_sfx.set_volume(volume)
        self.splash_screen_sounds.set_volume(volume)

    def update_music_volume(self, volume: float):
        self.title_screen_music.set_volume(volume)