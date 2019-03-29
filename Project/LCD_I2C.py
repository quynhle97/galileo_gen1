import time
import sys
import mraa

# Ligth sensor & Led
LIGHT_SENSOR_PIN = 1
MAX_LIGHT = 70
LED_PWM_PIN = 5

# some const
# LCD Address
LCD_ADDRESS = 0x3f

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# offset for up to 4 rows
LCD_ROW_OFFSET = (0x80, 0xC0, 0x94, 0xD4)

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  # Enable bit
Rw = 0b00000010  # Read/Write bit
Rs = 0b00000001 # Register select bit

class lcd:
	#initializes objects and lcd
	def __init__(self):
		self.lcd_device = mraa.I2c(0)
		self.lcd_device.address(LCD_ADDRESS)	
		
		self.lcd_write(0x03)
	      	self.lcd_write(0x03)
      		self.lcd_write(0x03)
      		self.lcd_write(0x02)

		self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
      		self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
      		self.lcd_write(LCD_CLEARDISPLAY)
      		self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
      		time.sleep(0.2)

	# clocks EN to latch command
	def lcd_strobe(self, data):
	      	self.lcd_device.writeByte(data | En | LCD_BACKLIGHT)
     	 	time.sleep(.0005)
      		self.lcd_device.writeByte(((data & ~En) | LCD_BACKLIGHT))
      		time.sleep(.0001)

	def lcd_write_four_bits(self, data):
      		self.lcd_device.writeByte(data | LCD_BACKLIGHT)
    	  	self.lcd_strobe(data)

	# write a command to lcd
   	def lcd_write(self, cmd, mode=0):
      		self.lcd_write_four_bits(mode | (cmd & 0xF0))
      		self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

	# put string function
	def lcd_display_string(self, string, line):
      		if line == 1:
         		self.lcd_write(0x80)
      		if line == 2:
         		self.lcd_write(0xC0)
      		if line == 3:
         		self.lcd_write(0x94)
      		if line == 4:
         		self.lcd_write(0xD4)

      		for char in string:
         		self.lcd_write(ord(char), Rs)	
	
	# define backlight on/off (lcd.backlight(1); off= lcd.backlight(0)
   	def backlight(self, state): # for state, 1 = on, 0 = off
      		if state == 1:
         		self.lcd_device.write_cmd(LCD_BACKLIGHT)
      		elif state == 0:
			self.lcd_device.write_cmd(LCD_NOBACKLIGHT)

	# define precise positioning (addition from the forum)
   	def lcd_display_string_pos(self, string, line, pos):
    		if line == 1:
      			pos_new = pos
    		elif line == 2:
      			pos_new = 0x40 + pos
    		elif line == 3:
      			pos_new = 0x14 + pos
    		elif line == 4:
			pos_new = 0x54 + pos		
	
		self.lcd_write(0x80 + pos_new)
	
		for char in string:
			self.lcd_write(ord(char), Rs)

	# clear lcd and set to home
   	def lcd_clear(self):
     	 	self.lcd_write(LCD_CLEARDISPLAY)
      		self.lcd_write(LCD_RETURNHOME)

	
	
