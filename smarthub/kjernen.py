from SignalFraRaspberryIpTilArduino import sendSignalToArduino, clearLCD
from

#Knappe variabler
alarm_time = 0
visit_time = 0

#Alarm variabler
hours = 0
minutes = 0
alarm_state = f"{hours}:{minutes}"

def update_alarm(encoder):
    if editAlarm_mode == 1:
        if set_alarm == 0:
            hours = encoder.read() % 24
            if hours < 10:
                hours = "0" + hours

        elif set_alarm == 1:
            minutes = encoder.read() % 60
            if minutes < 10:
                minutes = "0" + minutes

def volume_control(encoder):


while True:
    alarm_mode =
    editAlarm_mode =
    visit_mode =

    if type() == int():
        volume_control(encoder)

    elif

    if alarm_mode = 1 && alarm_time == 0:
        alarm_time = 1

    elif alarm_mode = 1 && alarm_time == 1:
        alarm_time = 0

    elif editAlarm_mode = 1 && editAlarm == 0:
        update_alarm(encoder)
        time = f"{hours}:{minutes}"
        sendSignalToArduino(time, 0, 0)
        editAlarm = 1

    elif editAlarm_mode = 1 && editAlarm == 1:
        clearLCD()
        editAlarm = 0

    elif visit_mode = 1 && visit_time == 0:
        sendSignalToArduino("Besøks tid", 7, 1)
        visit_time = 1

    elif visit_mode = 1 && visit_time == 1:
        clearLCD()
        visit_time = 0