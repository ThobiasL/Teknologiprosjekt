from adapters.headunit_wireless_communication import Wireless_communication
from adapters.headunit_arduino import ArduinoSerial
from services.headunit import Headunit
from adapters.sound_player import SoundPlayer
from time import sleep, strftime

# kaller på funksjonene fra klassen ArduinoSerial
arduino = ArduinoSerial()

# kaller på funksjonene fra klassen Wireless_communication
wireless = Wireless_communication()
