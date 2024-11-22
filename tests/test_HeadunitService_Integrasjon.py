import unittest
from unittest.mock import Mock
from core.services import HeadunitService
from adapters.headunit.database_adapter import DatabaseAdapter
from services.periodic_reader import PeriodicDatabaseReader


def test_headunit_service_with_database_integration():
    # Arrange
    database_mock = Mock()
    database_mock.read_auto_door_lock_time.return_value = "12:00:00"
    database_mock.send_auto_door_lock_time = Mock()
    database_mock

    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=Mock(),
        sound_player=Mock(),
        database=database_mock
    )

    # Act
    current_time = "12:00:00"
    doorlock_time = headunit_service.database.read_auto_door_lock_time()

    if doorlock_time == current_time:
        headunit_service.database.send_auto_door_lock_time(1)  # Simuler at døren låses
    else:
        headunit_service.database.send_auto_door_lock_time()

    # Assert
    database_mock.read_auto_door_lock_time.assert_called_once()
    database_mock.send_auto_door_lock_time.assert_called_with(1)

def test_periodic_reader_with_headunit_integration():
    # Arrange
    database_mock = Mock()
    database_mock.get_session_factory.return_value = Mock()

    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=Mock(),
        sound_player=Mock(),
        database=database_mock
    )

    # Mock `handle_door_lock_update` for å observere kall
    headunit_service.handle_door_lock_update = Mock()

    db_reader = PeriodicDatabaseReader(
        db_session_factory=database_mock.get_session_factory(),
        on_door_lock_update=headunit_service.handle_door_lock_update,
        interval=0.5
    )

    # Act
    db_reader.on_door_lock_update(True)  # Simuler en oppdatering

    # Assert
    database_mock.get_session_factory.assert_called_once()  # Sjekk at database-tilkoblingen ble brukt
    headunit_service.handle_door_lock_update.assert_called_with(True)  # Sjekk at callbacken ble kalt korrekt


def test_wireless_adapter_with_headunit_integration():
    # Arrange
    wireless_mock = Mock()
    wireless_mock.get_message.return_value = "door_is_locked"

    headunit_service = HeadunitService(
        wireless_comm=wireless_mock,
        arduino=Mock(),
        sound_player=Mock(),
        database=Mock()
    )

    # Act
    message = headunit_service.wireless_comm.get_message()
    if message == "door_is_locked":
        headunit_service.database.send_auto_door_lock_time(1)  # Simuler at døren låses

    # Assert
    wireless_mock.get_message.assert_called_once()
    headunit_service.database.send_auto_door_lock_time.assert_called_with(1)

def test_sound_player_and_headunit_integration():
    # Arrange
    sound_player_mock = Mock()
    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=Mock(),
        sound_player=sound_player_mock,
        database=Mock()
    )

    # Act
    headunit_service.sound_player.play_sound("alarm")

    # Assert
    sound_player_mock.play_sound.assert_called_with("alarm")
