import pygame
import os
from sq_src.metas import SingletonMeta
import random
import time
from sq_src.singletons.user_data import UserData
from sq_src.configs import MUSIC_FADE_EVENT


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

        self.is_music_on: bool = False
        #music fade variables
        self.n_steps = 100
        self.volume_step_size = 0
        self.sleep_duration = 0

    def PlayRandomSlideSfx(self):
        """
        Plays a random sliding sound effect.
        """
        sfx = random.choice(self.slide_sfxs)
        sfx.play()
    
    def FadeOutTitleScreenMusic(self, fade_duration_ms: int = 6000):
        """
        Fades out the currently playing title screen music over a specified duration.

        Args:
            fade_duration_ms (int, optional): The duration of the fade out in milliseconds (default: 3000).
        """
        #fade_out_sound(self.title_screen_music, fade_duration_ms)
        self.is_music_on = False
        original_volume = self.title_screen_music.get_volume()
        self.volume_step_size = original_volume / self.n_steps
        self.sleep_duration = fade_duration_ms // self.n_steps
        #pygame.event.Event()
        pygame.time.set_timer(MUSIC_FADE_EVENT, self.sleep_duration, self.n_steps)

    def FadeInTitleScreenMusic(self):
        """
        Fade in the title screen music.
        """
        self.title_screen_music.stop()#stop the sound it had previously faded out (is still playing but volume is 0)
        self.title_screen_music.set_volume(self.current_music_volume)#restore volume if the music had been faded out
        self.title_screen_music.play(fade_ms=5000, loops=-1)
        self.is_music_on = True

    
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

    def update(self, events: list[pygame.event.Event]):
        """
        Handles events for the game audio.
        """

        for event in events:
            if event.type == MUSIC_FADE_EVENT and self.is_music_on==False:
                original_volume = self.title_screen_music.get_volume()
                new_volume = original_volume - self.volume_step_size
                if new_volume<0:#just in case to make sure the volume doesn't go negative
                    new_volume = 0
                self.title_screen_music.set_volume(new_volume)