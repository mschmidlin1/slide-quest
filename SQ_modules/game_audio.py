import pygame
import os
from SQ_modules.metas import SingletonMeta
import random
import time
from SQ_modules.UserData import UserData

def fade_out_sound(sound: pygame.mixer.Sound, fade_duration_ms: int):
    """
    Gradually fades out the volume of a pygame sound object over a specified duration in milliseconds.

    Args:
        sound (pygame.mixer.Sound): The sound object to fade out.
        fade_duration_ms (int): The duration of the fade out in milliseconds.
    """
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
    """
    This class manages all audio playback within the game, including sound effects and music.

    Attributes:
        current_music_volume (float): The current volume level for music (0.0 to 1.0).
        current_sfx_volume (float): The current volume level for sound effects (0.0 to 1.0).
        slide_sfxs (list[pygame.mixer.Sound]): A list of loaded sound effects for slide transitions.
        level_complete_sfx (pygame.mixer.Sound): The sound effect played when a level is completed.
        title_screen_music (pygame.mixer.Sound): The music played on the title screen.
        button_click_sfx (pygame.mixer.Sound): The sound effect played when a button is clicked.
        splash_screen_sounds (pygame.mixer.Sound): The sound effects played on the splash screen.
    """
    def __init__(self):
        """
        Initializes the GameAudio class and loads all sound effects and music.
        """
        pygame.mixer.init()
        self.user_data = UserData()
        self.current_music_volume = self.user_data.user_data['volume_levels']['music']
        self.current_sfx_volume = self.user_data.user_data['volume_levels']['sfx']

        slide_sounds_dir = "resources/audio/sounds/SlideSounds"
        self.slide_sfxs: list[pygame.mixer.Sound] = []
        for sound_file in os.listdir(slide_sounds_dir):
            sfx = pygame.mixer.Sound(os.path.join(slide_sounds_dir, sound_file))
            sfx.set_volume(self.current_sfx_volume)
            self.slide_sfxs.append(sfx)


        self.level_complete_sfx = pygame.mixer.Sound("resources/audio/sounds/LevelCompleteSound.mp3")
        self.level_complete_sfx.set_volume(self.current_sfx_volume)
        self.title_screen_music = pygame.mixer.Sound("resources/audio/music/PhilosophicalSongTitle - RoccoW  Chiptune [No Copyright Music].mp3")
        self.title_screen_music.set_volume(self.current_music_volume)
        self.button_click_sfx = pygame.mixer.Sound("resources/audio/sounds/multi-pop.mp3")
        self.button_click_sfx.set_volume(self.current_sfx_volume)
        self.splash_screen_sounds = pygame.mixer.Sound("resources/audio/sounds/vibes-windy-whoosh-magical-chimes.mp3")
        self.splash_screen_sounds.set_volume(self.current_sfx_volume)

    def PlayRandomSlideSfx(self):
        """
        Plays a random sliding sound effect.
        """
        sfx = random.choice(self.slide_sfxs)
        sfx.play()
    
    def FadeOutMusic(self, fade_duration_ms: int = 3000):
        """
        Fades out the currently playing title screen music over a specified duration.

        Args:
            fade_duration_ms (int, optional): The duration of the fade out in milliseconds (default: 3000).
        """
        fade_out_sound(self.title_screen_music, fade_duration_ms)
    
    def update_sfx_volume(self, volume: float):
        """
        Updates the volume for all sound effects in the game.

        This method sets the new volume level for all loaded sound effects, including those for slide transitions,
        level completion, button clicks, and splash screen sounds.

        Args:
            volume (float): The new volume level for sound effects (0.0 to 1.0).
        """
        self.current_sfx_volume = volume
        self.level_complete_sfx.set_volume(volume)
        for sfx in self.slide_sfxs:
            sfx.set_volume(volume)
        self.button_click_sfx.set_volume(volume)
        self.splash_screen_sounds.set_volume(volume)

    def update_music_volume(self, volume: float):
        """
        Updates the volume for all music tracks in the game.

        This method sets the new volume level for music tracks, currently affecting only the title screen music. 
        It allows dynamic adjustment of the music volume based on user preferences or other in-game events.

        Args:
            volume (float): The new volume level for music (0.0 to 1.0).
        """
        self.current_music_volume = volume
        self.title_screen_music.set_volume(volume)