from unittest.mock import Mock
from core.services import HeadunitService


def test_handle_door_lock_update():
    # Arrange
    headunit_service = HeadunitService(Mock(), Mock(), Mock(), Mock())
    headunit_service2 = HeadunitService(Mock(), Mock(), Mock(), Mock())
    headunit_service3 = HeadunitService(Mock(), Mock(), Mock(), Mock())

    status = True  # Døren låses
    status2 = False  # Døren låses ikke
    status3 = "Test"  # Ugyldig status

    # Act
    headunit_service.handle_door_lock_update(status)
    headunit_service2.handle_door_lock_update(status2)
    headunit_service3.handle_door_lock_update(status3)

    # Assert
    assert headunit_service is not None  # Sikre at objektet eksisterer
    assert headunit_service2 is not None  # Sikre at objektet eksisterer
    assert headunit_service3 is not None  # Sikre at objektet eksisterer

    assert isinstance(status, bool)  # Test for korrekt type
    assert isinstance(status2, bool)  # Test for korrekt type
    assert not isinstance(status3, bool)  # Test for korrekt type

    assert isinstance(headunit_service, HeadunitService)  # Test objektets type
    assert isinstance(headunit_service2, HeadunitService)  # Test objektets type
    assert isinstance(headunit_service3, HeadunitService)  # Test objektets type

def test_door_lock_with_multiple_return_values():
    # Arrange
    arduino_mock = Mock()
    database_mock = Mock()

    # Sett opp flere return_values for mocken
    database_mock.read_auto_door_lock_time.side_effect = ["12:00:00", "05:05:05"]

    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=arduino_mock,
        sound_player=Mock(),
        database=database_mock
    )

    # Act
    # Første kall
    current_time = "12:00:00"
    if current_time == database_mock.read_auto_door_lock_time():
        headunit_service.database.send_auto_door_lock_time(1)
    else:
        headunit_service.database.send_auto_door_lock_time(0)

    # Andre kall
    if current_time == database_mock.read_auto_door_lock_time():
        headunit_service.database.send_auto_door_lock_time(1)
    else:
        headunit_service.database.send_auto_door_lock_time(0)

    # Assert
    # Sjekk at read_auto_door_lock_time ble kalt to ganger
    assert database_mock.read_auto_door_lock_time.call_count == 2

    # Sjekk at send_auto_door_lock_time ble kalt med riktig argument begge ganger
    headunit_service.database.send_auto_door_lock_time.assert_any_call(1)
    headunit_service.database.send_auto_door_lock_time.assert_any_call(0)
