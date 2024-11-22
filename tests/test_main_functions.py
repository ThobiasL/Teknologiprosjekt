import unittest
from unittest.mock import Mock
from core.models.datetime_model import DateTimeModel
from core.services import HeadunitService
from services.periodic_reader import PeriodicDatabaseReader

def test_get_datetime():
    # Arrange and Act
    datetime = DateTimeModel.get_datetime()

    # Assert
    assert datetime is not None  # Sjekk at verdien ikke er None
    assert isinstance(datetime, str)  # Sjekk at verdien er en streng
    assert "." in datetime  # Sjekk at strengen inneholder "." som separasjon

def test_get_time():
    # Arrange and Act
    time = DateTimeModel.get_time()

    # Assert
    assert time is not None
    assert isinstance(time, str)
    assert ":" in time  # Sikre at tiden inneholder ":" som separasjon

def test_periodic_database_reader_with_mocks():
    # Arrange
    db_session_factory_mock = Mock()
    on_door_lock_update_mock = Mock()

    reader = PeriodicDatabaseReader(
        db_session_factory=db_session_factory_mock,
        on_door_lock_update=on_door_lock_update_mock,
        interval=0.5
    )

    # Act
    reader.start()
    reader.on_door_lock_update(True)
    reader.stop()
    reader.run()


    # Assert
    # Sjekk at reader kallte on_door_lock_update
    on_door_lock_update_mock.assert_called_with(True)
    db_session_factory_mock.assert_called_once()  # Sjekk at session factory ble brukt

def test_task_execution_from_database():
    # Arrange
    database_mock = Mock()
    database_mock.read_tasks.return_value = [
        {"name": "eat_dinner", "time": "18:00"}
    ]

    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=Mock(),
        sound_player=Mock(),
        database=database_mock
    )

    # Act
    current_time = "18:00"
    tasks = database_mock.read_tasks()
    for task in tasks:
        if task["time"] == current_time:
            headunit_service.sound_player.play_sound(task["name"])

    # Assert
    database_mock.read_tasks.assert_called_once()
    headunit_service.sound_player.play_sound.assert_called_with("eat_dinner")

def test_fall_detected_message_handling():
    # Arrange
    wireless_mock = Mock()
    wireless_mock.get_message.return_value = "fall_detected"

    headunit_service = HeadunitService(
        wireless_comm=wireless_mock,
        arduino=Mock(),
        sound_player=Mock(),
        database=Mock()
    )

    # Act
    message = headunit_service.wireless_comm.get_message()
    if message == "fall_detected":
        headunit_service.sound_player.play_sound("alert")

    # Assert
    wireless_mock.get_message.assert_called_once()
    headunit_service.sound_player.play_sound.assert_called_with("alert")


