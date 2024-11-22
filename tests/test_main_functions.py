import unittest
from unittest.mock import Mock
from core.models.datetime_model import DateTimeModel
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




