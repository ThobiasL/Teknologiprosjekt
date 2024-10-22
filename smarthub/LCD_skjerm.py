import digitalio
import board
import adafruit_character_lcd.character_lcd as characterlcd
import RPi.GPIO as GPIO
from time import sleep, strftime

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

datetime = strftime("%d:%m")

def update_datetime():
    lcd.move_to(0,0)
    full_datetime = strftime("%d.%m.%y %H:%M")
    lcd.message = full_datetime

def lcd_update():