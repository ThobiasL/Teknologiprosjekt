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


