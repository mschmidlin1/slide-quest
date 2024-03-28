import pygame
import os
from SQ_modules.configs import GAME_VOLUME




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