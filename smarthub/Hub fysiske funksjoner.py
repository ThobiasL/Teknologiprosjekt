# Her blir alle nødvendige biblioterker inprotert.
import digitalio
import board
import adafruit_character_lcd.character_lcd as characterlcd
import Encoder
import RPi.GPIO as GPIO
from time import sleep, strftime

from PyQt6.QtGui.QTextCursor import position

GPIO.setmode(GPIO.BCM)

# Setter opp LCD-skjermen
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d7 = digitalio.DigitalInOut(board.D27)
lcd_d6 = digitalio.DigitalInOut(board.D22)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_backlight = digitalio.DigitalInOut(board.D4)

lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)
lcd_backlight = True
lcd.clear()

lcd.move_to(0,0)
full_datetime = strftime("%d.%m.%y")
lcd.message = full_datetime

datetime = strftime("%d:%m")


# Setter opp knapper
# knapp for at den pårørende kan be om besøk (besøks tid)
pin_besok = digitalio.DigitalInOut(board.D18)# (GP 18)
pin_besok.direction = digitalio.Direction.INPUT
pin_besok.pull = digitalio.Pull.UP
besok_button_state = 0

# knapp for å bytte mellom timer og minuter i alarm systemet
pin_alarm = digitalio.DigitalInOut(board.D17)# (GP 17)
pin_alarm.direction = digitalio.Direction.INPUT
pin_alarm.pull = digitalio.Pull.UP
button_alarm_state = 0
alarm_state = f"{hours}:{minutes}"
hours = 0
minutes = 0

# Knapp for å avslutte eller starte alarm systemet
pin_edit = digitalio.DigitalInOut(board.D27)# (GP 27)
pin_edit.direction = digitalio.Direction.INPUT
pin_edit.pull = digitalio.Pull.UP
button_edit_state = 0
edit_alarm = 0
set_alarm = 0
alarm = 0


# Setter opp encoder
encoder = Encoder.Encoder(14, 15)

def update_alarm(encoder):
    previous_position = -1
    position = encoder.read()
    while position != previous_position:
        position = encoder.read()
        if edit_alarm == 1:
            if set_alarm == 0:
                hours = encoder.read() % 24
                if hours < 10:
                    hours = "0" + hours

            elif set_alarm == 1:
                minutes = encoder.read() % 60
                if minutes < 10:
                    minutes = "0" + minutes

            #if lcd.move_to(0,1):
             #   position = encoder.read() % len(hourlist)
              #  lcd.message = position
            #else:
             #   position = encoder.read() % len(minutelist)
              #  lcd.message = position
        elif edit_alarm == 0:
            position = encoder.read() % 100

        previous_position = position
        time.sleep(0.1)

while True:

    button_besok = pin_besok.value
    button_alarm = pin_alarm.value
    button_edit = pin_edit.value

    if button_besok != besok_button_state:
        if button_besok == 1:
            #with open(filnavn.jason, 'w') as file:
                #write(besøks_tid = True)
            lcd.move_to(7,1)
            lcd.message = "Besøks tid"
        besok_button_state = button_besok
        time.sleep(0.01)

    if button_alarm != button_alarm_state:
        if button_alarm == 1 and button_alarm_state == 0:
            set_alarm = 1
        elif button_alarm == 1 and button_alarm_state == 1:
            set_alarm = 0
        button_alarm_state = button_alarm
        time.sleep(0.01)

    if button_edit != button_edit_state:
        if button_edit == 1 and button_edit_state == 0:
            edit_alarm = 1
        elif button_edit == 1 and button_edit_state == 1:
            edit_alarm = 0
        button_edit_state = button_edit
        time.sleep(0.01)

    if alarm_state == datetime:
        alarm = 1
        lcd.move_to(7,1)
        lcd.message = "Alarm"



    update_alarm(encoder)
    lcd.move_to(0,1)
    lcd.message = alarm_state