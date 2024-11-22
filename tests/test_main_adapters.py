from unittest.mock import Mock, patch, call
import serial
from adapters.headunit.wireless_communication_adapter import WirelessCommunicationAdapter
from adapters.headunit.arduino_adapter import ArduinoAdapter
from adapters.headunit.database_adapter import DatabaseAdapter

# Tester at get_message-metoden til WirelessCommunicationAdapter returnerer korrekte meldinger.
def test_wirelessCommunicationAdapter_get_message():
    # Arrange
    adapter = WirelessCommunicationAdapter()
    adapter2 = WirelessCommunicationAdapter()
    adapter3 = WirelessCommunicationAdapter()
    adapter4 = WirelessCommunicationAdapter()
    adapter5 = WirelessCommunicationAdapter()

    adapter.get_message = Mock(return_value="door_is_locked")
    adapter2.get_message = Mock(return_value="door_is_unlocked")
    adapter3.get_message = Mock(return_value="fall_detected")
    adapter4.get_message = Mock(return_value="false_alarm")
    adapter5.get_message = Mock(return_value="Pills_Dispens")

    # Act
    message = adapter.get_message()
    message2 = adapter2.get_message()
    message3 = adapter3.get_message()
    message4 = adapter4.get_message()
    message5 = adapter5.get_message()

    # Assert
    assert message == "door_is_locked"
    assert message2 == "door_is_unlocked"
    assert message3 == "fall_detected"
    assert message4 == "false_alarm"
    assert message5 == "Pills_Dispens"

# Verifiserer at close-metoden kalles én gang på flere adaptere
# (WirelessCommunicationAdapter, ArduinoAdapter, SoundPlayerAdapter, DatabaseAdapter og db_reader).
def test_wirelessCommunicationAdapter_close():
    # Arrange
    wireless_adapter = Mock()
    arduino_adapter = Mock()
    sound_player_adapter = Mock()
    database_adapter = Mock()
    db_reader = Mock()

    # Act
    wireless_adapter.close()
    arduino_adapter.close()
    sound_player_adapter.close()
    database_adapter.close()
    db_reader.close()

    # Assert
    wireless_adapter.close.assert_called_once()
    arduino_adapter.close.assert_called_once()
    sound_player_adapter.close.assert_called_once()
    database_adapter.close.assert_called_once()
    db_reader.close.assert_called_once()

# Mock-metoder og serial.Serial brukes til å teste at send_signal-metoden til ArduinoAdapter kalles med riktige argumenter.
# Metoden testes for flere adapterinstanser. Testen verifiserer også at serial.Serial-objektene opprettes korrekt.
@patch('adapters.headunit.headunit_arduino.serial.Serial', autospec=True)
def test_arduinoAdapter_send_signal(mock_serial):
    # Arrange: Mock en instans av Serial
    mock_serial_instance = mock_serial.return_value
    adapter = ArduinoAdapter(port="COM3", baudrate=9600)  # Bruk Windows-portnavn
    adapter2 = ArduinoAdapter(port="COM3", baudrate=9600)
    adapter3 = ArduinoAdapter(port="COM3", baudrate=9600)

    adapter.send_signal = Mock()
    adapter2.send_signal = Mock()
    adapter3.send_signal = Mock()

    # Act
    adapter.send_signal("TestSignal-1", 0, 0)
    adapter2.send_signal("TestSignal-2", 1, 0)
    adapter3.send_signal("TestSignal-3", 5, 1)

    # Assert
    adapter.send_signal.assert_called_with("TestSignal-1", 0, 0)
    adapter2.send_signal.assert_called_with("TestSignal-2", 1, 0)
    adapter3.send_signal.assert_called_with("TestSignal-3", 5, 1)

    # Verifiser at Serial ble opprettet riktig
    mock_serial.assert_has_calls([
        call("COM3", 9600),
        call("COM3", 9600),
        call("COM3", 9600),
    ])

# Tester read_signal-metoden i ArduinoAdapter ved å mocke ulike signaler som kan mottas.
# Testen sjekker at de returnerte verdiene samsvarer med forventningene, og at serial.Serial opprettes riktig.
@patch('adapters.headunit.headunit_arduino.serial.Serial', autospec=True)
def test_arduinoAdapter_read_signal(mock_serial):
    # Arrange: Mock en instans av Serial
    mock_serial_instance = mock_serial.return_value
    adapter = ArduinoAdapter(port="COM3", baudrate=9600)
    adapter2 = ArduinoAdapter(port="COM3", baudrate=9600)
    adapter3 = ArduinoAdapter(port="COM3", baudrate=9600)

    # Mock read_signal-metoden
    adapter.read_signal = Mock(return_value="TestSignal")
    adapter2.read_signal = Mock(return_value="1+1=2")
    adapter3.read_signal = Mock(return_value="False")

    # Act
    signal = adapter.read_signal()
    signal2 = adapter2.read_signal()
    signal3 = adapter3.read_signal()

    # Assert
    assert signal == "TestSignal"
    assert signal2 == "1+1=2"
    assert signal3 == "False"

    # Verifiser at Serial ble opprettet riktig for alle instanser
    mock_serial.assert_has_calls([
        call("COM3", 9600),
        call("COM3", 9600),
        call("COM3", 9600),
    ])

# Tester read_auto_door_lock_time-metoden i DatabaseAdapter.
# Mock-metoder brukes til å simulere ulike tidspunkter for automatisk låsing. Testen sjekker at de returnerte verdiene er som forventet.
def test_databaseAdapter_read_auto_door_lock_time():
    # Arrange
    adapter = DatabaseAdapter()
    adapter2 = DatabaseAdapter()
    adapter3 = DatabaseAdapter()

    adapter.read_auto_door_lock_time = Mock(return_value="12:00")
    adapter2.read_auto_door_lock_time = Mock(return_value="05:05")
    adapter3.read_auto_door_lock_time = Mock(return_value="00:00")

    # Act
    lock_time = adapter.read_auto_door_lock_time()
    lock_time2 = adapter2.read_auto_door_lock_time()
    lock_time3 = adapter3.read_auto_door_lock_time()

    # Assert
    assert lock_time == "12:00"
    assert lock_time2 == "05:05"
    assert lock_time3 == "00:00"


