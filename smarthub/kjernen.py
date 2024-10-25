from smarthub.LCD_skjerm import lcd, datetime, lcd_update, update_datetime
from smarthub.Rotary_encoder import encoder, read_encoder
from smarthub.Buttons import pin_besok, pin_alarm, pin_edit

#klar gjøring av LCD-skjerm
lcd_backlight = True
lcd.clear()

#Knappe variabler
besok_button_state = 0
button_alarm_state = 0
button_edit_state = 0
edit_alarm = 0
set_alarm = 0
alarm = 0

#Alarm variabler
hours = 0
minutes = 0
alarm_state = f"{hours}:{minutes}"

def update_alarm(encoder):
    if edit_alarm == 1:
        if set_alarm == 0:
            hours = encoder.read() % 24
            if hours < 10:
                hours = "0" + hours

        elif set_alarm == 1:
            minutes = encoder.read() % 60
            if minutes < 10:
                minutes = "0" + minutes

while True:
    button_besok = pin_besok.value
    button_alarm = pin_alarm.value
    button_edit = pin_edit.value