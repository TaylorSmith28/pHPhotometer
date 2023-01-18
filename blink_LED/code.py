"""Display a custom character"""
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Metro M0/M4 Pin Config:
lcd_rs = digitalio.DigitalInOut(board.GP15)
lcd_en = digitalio.DigitalInOut(board.GP14)
lcd_d7 = digitalio.DigitalInOut(board.GP10)
lcd_d6 = digitalio.DigitalInOut(board.GP11)
lcd_d5 = digitalio.DigitalInOut(board.GP12)
lcd_d4 = digitalio.DigitalInOut(board.GP13)

# Initialise the LCD class
lcd = characterlcd.Character_LCD(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

lcd.message = "Hello\nCircuitPython"
