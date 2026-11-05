import unittest

from sq_src.data_structures.game_enums import Direction, Screen
from sq_src.window import Window


class _Silent:
    def log_info(self, _message):
        return None

    def play(self):
        return None


class TestLeaveGameForTitle(unittest.TestCase):
    def test_title_button_does_not_read_missing_stars(self):
        """Leaving an unfinished level must not touch Game.stars."""
        window = Window.__new__(Window)
        window.current_screen_type = Screen.OPTIONS
        window.navigation_manager = type("Nav", (), {"current_screen": Screen.TITLE, "game_active": True})()
        window.logging_service = _Silent()
        window.game_audio = type("Audio", (), {"is_music_on": True, "button_click_sfx": _Silent()})()
        window.current_game = type("Game", (), {"shortest_path": [Direction.RIGHT]})()
        window.title_screen = "title"
        saved = {}

        def save_seed(path, completed, time_ms, num_moves, stars=0):
            saved["args"] = (path, completed, time_ms, num_moves, stars)

        window.level_manager = type("Levels", (), {"save_seed": staticmethod(save_seed)})()

        window.handle_navigation()

        self.assertEqual(saved["args"], ([Direction.RIGHT], False, 0, 0, 0))
        self.assertIsNone(window.current_game)
        self.assertFalse(window.navigation_manager.game_active)
        self.assertIs(window.current_screen, window.title_screen)
        self.assertEqual(window.current_screen_type, Screen.TITLE)
