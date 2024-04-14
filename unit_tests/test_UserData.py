import unittest
from SQ_modules.UserData import UserData
from SQ_modules.configs import GAME_VOLUME
import os
from SQ_modules.Metas import SingletonMeta
from SQ_modules.GameEnums import GameDifficulty

class Test_UserData(unittest.TestCase):
    
    def test_1setUp(self):
        """Ensure each test starts with a clean slate."""
        # Ensure any existing file is removed
        if os.path.exists(UserData.file_name):
            os.remove(UserData.file_name)
        # Resetting the singleton instance for testing (not implemented in given class, consider adding)
        SingletonMeta._instances = {}

    def test_singleton_instance(self):
        """Test that only one instance of UserData can be created."""
        instance1 = UserData()
        instance2 = UserData()
        self.assertIs(instance1, instance2)

    def test_write_and_read(self):
        """Test writing to and reading from the file."""
        user_data = UserData()
        user_data.update_music_volume(0.30)
        user_data.update_sfx_volume(0.40)
        del user_data  # Delete the instance to test reading from file
        
        # Create a new instance which should load from file
        new_user_data = UserData()
        self.assertEqual(new_user_data.user_data['volume_levels']['music'], 0.30)
        self.assertEqual(new_user_data.user_data['volume_levels']['sfx'], 0.40)

    def test_update_music_volume(self):
        """Test the update_music_volume method."""
        user_data = UserData()
        user_data.update_music_volume(0.25)
        self.assertEqual(user_data.user_data['volume_levels']['music'], 0.25)

    def test_update_sfx_volume(self):
        """Test the update_sfx_volume method."""
        user_data = UserData()
        user_data.update_sfx_volume(0.75)
        self.assertEqual(user_data.user_data['volume_levels']['sfx'], 0.75)

    def test_add_completed_level(self):
        """Test the add_completed_level method."""
        user_data = UserData()
        user_data.add_completed_level(GameDifficulty.BEGINNER, 1)
        self.assertIn(1, user_data.user_data['completed_maps'][GameDifficulty.BEGINNER])


if __name__ == '__main__':
    unittest.main()