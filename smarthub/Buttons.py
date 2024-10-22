import digitalio
import board
import RPi.GPIO as GPIO

# Setter opp knapper
# knapp for at den pårørende kan be om besøk (besøks tid)
pin_besok = digitalio.DigitalInOut(board.D5)# (GP 5)
pin_besok.direction = digitalio.Direction.INPUT
pin_besok.pull = digitalio.Pull.UP
besok_button_state = 0

# knapp for å bytte mellom timer og minuter i alarm systemet
pin_alarm = digitalio.DigitalInOut(board.D6)# (GP 6)
pin_alarm.direction = digitalio.Direction.INPUT
pin_alarm.pull = digitalio.Pull.UP
button_alarm_state = 0
hours = 0
minutes = 0
alarm_state = f"{hours}:{minutes}"

# Knapp for å avslutte eller starte alarm systemet
pin_edit = digitalio.DigitalInOut(board.D16)# (GP 16)
pin_edit.direction = digitalio.Direction.INPUT
pin_edit.pull = digitalio.Pull.UP
button_edit_state = 0
edit_alarm = 0
set_alarm = 0
alarm = 0