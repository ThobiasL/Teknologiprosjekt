from unittest.mock import Mock
from adapters.headunit.database_adapter import DatabaseAdapter
from adapters.headunit.sound_player_adapter import SoundPlayerAdapter

def test_databaseAdapter_send_auto_door_lock_time():
    # Arrange
    adapter = DatabaseAdapter()
    adapter2 = DatabaseAdapter()

    adapter.send_auto_door_lock_time = Mock()
    adapter2.send_auto_door_lock_time = Mock()

    # Act
    adapter.send_auto_door_lock_time(1)
    adapter2.send_auto_door_lock_time(0)

    # Assert
    adapter.send_auto_door_lock_time.assert_called_with(1)
    adapter2.send_auto_door_lock_time.assert_called_with(0)

def test_SoundPlayerAdapter_play_sound():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.play_sound = Mock()

    # Act
    adapter.play_sound("alarm")
    #adapter.player
    #adapter.play_sound("eat_dinner")

    # Assert
    adapter.play_sound.assert_called_with("alarm")


def test_pause_sound():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.pause_sound = Mock()

    # Act
    adapter.pause_sound()

    # Assert
    adapter.pause_sound.assert_called_once()

def test_unpause_sound():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.unpause_sound = Mock()

    # Act
    adapter.unpause_sound()

    # Assert
    adapter.unpause_sound.assert_called_once()

def test_stop_sound():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.stop_sound = Mock()

    # Act
    adapter.stop_sound()

    # Assert
    adapter.stop_sound.assert_called_once()

def test_play_alarm():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.play_alarm = Mock()

    # Act
    adapter.play_alarm()

    # Assert
    adapter.play_alarm.assert_called_once()

def test_stop_alarm():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.stop_alarm = Mock()

    # Act
    adapter.stop_alarm()

    # Assert
    adapter.stop_alarm.assert_called_once()

def test_get_alarm():
    # Arrange
    adapter = SoundPlayerAdapter()
    adapter.get_alarm = Mock(return_value="Alarm")

    # Act
    alarm = adapter.get_alarm()

    # Assert
    assert alarm == "Alarm"


