import LCD_I2C
from time import *

lcd = LCD_I2C.lcd()

lcd.lcd_display_string("hello world", 1)
lcd.lcd_display_string_pos("galileo 1", 2, 3)
