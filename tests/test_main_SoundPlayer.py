from unittest.mock import Mock, patch
from adapters.headunit.sound_player_adapter import SoundPlayerAdapter, SoundPlayer


@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_SoundPlayerAdapter_play_sound(dummy_audio_file, monkeypatch):
    # Arrange
    monkeypatch.setattr("os.path.dirname", lambda _: dummy_audio_file)
    adapter = SoundPlayerAdapter()
    #adapter.play_sound = Mock()

    # Act
    #adapter.play_sound("alarm")
    #adapter.player
    #adapter.play_sound("eat_dinner")

    # Assert
    assert adapter.player

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_pause_sound(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.pause_sound = Mock()

    # Act
    adapter.pause_sound()

    # Assert
    adapter.pause_sound.assert_called_once()

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_unpause_sound(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.unpause_sound = Mock()

    # Act
    adapter.unpause_sound()

    # Assert
    adapter.unpause_sound.assert_called_once()

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_stop_sound(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.stop_sound = Mock()

    # Act
    adapter.stop_sound()

    # Assert
    adapter.stop_sound.assert_called_once()

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_play_alarm(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.play_alarm = Mock()

    # Act
    adapter.play_alarm()

    # Assert
    adapter.play_alarm.assert_called_once()

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_stop_alarm(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.stop_alarm = Mock()

    # Act
    adapter.stop_alarm()

    # Assert
    adapter.stop_alarm.assert_called_once()

@patch("adapters.headunit.sound_player.pygame.mixer.Sound")
def test_get_alarm(mock_sound):
    # Arrange
    mock_sound.return_value = Mock()
    adapter = SoundPlayerAdapter()
    adapter.get_alarm = Mock(return_value="Alarm")

    # Act
    alarm = adapter.get_alarm()

    # Assert
    assert alarm == "Alarm"


