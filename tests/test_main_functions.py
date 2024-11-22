import unittest
from unittest.mock import Mock, MagicMock
from core.models.datetime_model import DateTimeModel
from core.services import HeadunitService
from services.periodic_reader import PeriodicDatabaseReader

# Tester at DateTimeModel.get_datetime() returnerer en gyldig strengrepresentasjon av dato og tid som ikke er None,
# og at den inneholder et punktum (".") som forventet formatseparasjon.
def test_get_datetime():
    # Arrange and Act
    datetime = DateTimeModel.get_datetime()

    # Assert
    assert datetime is not None  # Sjekk at verdien ikke er None
    assert isinstance(datetime, str)  # Sjekk at verdien er en streng
    assert "." in datetime  # Sjekk at strengen inneholder "." som separasjon

# Tester at DateTimeModel.get_time() returnerer en gyldig strengrepresentasjon av tid som ikke er None,
# og at den inneholder et kolon (":") som forventet formatseparasjon.
def test_get_time():
    # Arrange and Act
    time = DateTimeModel.get_time()

    # Assert
    assert time is not None
    assert isinstance(time, str)
    assert ":" in time  # Sikre at tiden inneholder ":" som separasjon

# Tester at PeriodicDatabaseReader: Kaller on_door_lock_update-funksjonen med riktig argument,
# Bruker db_session_factory nøyaktig én gang.
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

# Tester at HeadunitService leser oppgaver fra databasen og utfører riktig handling (spiller lyd)
# når gjeldende tid samsvarer med oppgavens planlagte tid.
def test_task_execution_from_database():
    # Arrange
    database_mock = Mock()
    database_mock.read_tasks.return_value = [
        {"name": "eat_dinner", "time": "18:00"},
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

# Tester at HeadunitService ikke utfører noen handling (spiller lyd)
# når gjeldende tid ikke samsvarer med noen av oppgavene som er lest fra databasen.
def test_no_task_execution_for_different_time():
    # Arrange
    database_mock = Mock()
    sound_player_mock = Mock()

    # Simuler oppgaver fra databasen
    database_mock.read_tasks.return_value = [
        {"name": "go_for_a_walk", "time": "10:00"},
    ]

    headunit_service = HeadunitService(
        wireless_comm=Mock(),
        arduino=Mock(),
        sound_player=sound_player_mock,
        database=database_mock
    )

    # Act
    current_time = "15:00"  # Simulerer at klokka er 15:00
    tasks = database_mock.read_tasks()

    for task in tasks:
        if task["time"] == current_time:
            headunit_service.sound_player.play_sound(task["name"])

    # Assert
    database_mock.read_tasks.assert_called_once()  # Verifiser at oppgaver ble lest fra databasen
    sound_player_mock.play_sound.assert_not_called()  # Sjekk at ingen lyd ble spilt

# Tester at HeadunitService korrekt mottar og prosesserer meldinger fra wireless_comm,
# og at meldingene returneres i forventet rekkefølge.
def test_message_processing_in_service():
    # Arrange
    wireless_mock = Mock()
    arduino_mock = Mock()
    sound_player_mock = Mock()
    database_mock = Mock()

    # Simuler en sekvens av meldinger
    wireless_mock.get_message.side_effect = [
        "door_is_locked",
        "door_is_unlocked",
        "fall_detected",
        "false_alarm",
        "Pills_Dispens"
    ]

    headunit_service = HeadunitService(
        wireless_comm=wireless_mock,
        arduino=Mock(),
        sound_player=Mock(),
        database=Mock()
    )

    # Act
    message1 = headunit_service.wireless_comm.get_message()
    message2 = headunit_service.wireless_comm.get_message()
    message3 = headunit_service.wireless_comm.get_message()
    message4 = headunit_service.wireless_comm.get_message()
    message5 = headunit_service.wireless_comm.get_message()


    # Assert
    assert message1 == "door_is_locked"
    assert message2 == "door_is_unlocked"
    assert message3 == "fall_detected"
    assert message4 == "false_alarm"
    assert message5 == "Pills_Dispens"

# Testen verifiserer at funksjonen handle_door_lock_update i HeadunitService oppdaterer dørstatusen (door_status)
# korrekt basert på input.
def test_handle_door_lock_update():
    # Arrange
    headunit_service = HeadunitService(Mock(), Mock(), Mock(), Mock())

    status_locked = True
    status_unlocked = False

    # Act
    headunit_service.handle_door_lock_update(status_locked)
    locked_status_result = headunit_service.door_status  # Etter første oppdatering

    # Assert
    assert locked_status_result is True, "Dørstatus bør settes til låst (True)"

    # Act (igjen)
    headunit_service.handle_door_lock_update(status_unlocked)
    unlocked_status_result = headunit_service.door_status  # Etter andre oppdatering

    # Assert
    assert unlocked_status_result is False, "Dørstatus bør settes til ulåst (False)"

# Denne testen verifiserer at en HeadunitService-instans blir riktig initialisert med de nødvendige adapterne.
def test_headunit_service_initialization():
    wireless_adapter = MagicMock()
    arduino_adapter = MagicMock()
    sound_player_adapter = MagicMock()
    database_adapter = MagicMock()

    service = HeadunitService(
        wireless_comm=wireless_adapter,
        arduino=arduino_adapter,
        sound_player=sound_player_adapter,
        database=database_adapter
    )

    assert service.wireless_comm == wireless_adapter
    assert service.arduino == arduino_adapter
    assert service.sound_player == sound_player_adapter
    assert service.database == database_adapter
