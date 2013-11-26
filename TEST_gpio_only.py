# LCD Test Script
# Script to test the input and output of the Raspberry Pi GPIO
#
# Author: Kevin Wong
#	With some code from a Raspberry Pi tutorial from:
#	http://www.youtube.com/watch?v=KM4n2OtwGl0
#
# Date: 11/10/2013

# The wiring for the LCD is as follows: 
# 1 : GND 
# 2 : 5V 
# 3 : Contrast (0-5V)* 
# 4 : RS (Register Select) 
# 5 : R/W (Read Write)       - GROUND THIS PIN! We do not want the LCD to send anything to the Pi @ 5v 
# 6 : Enable or Strobe 
# 7 : Data Bit 0             - NOT USED 
# 8 : Data Bit 1             - NOT USED 
# 9 : Data Bit 2             - NOT USED 
# 10: Data Bit 3             - NOT USED 
# 11: Data Bit 4 
# 12: Data Bit 5 
# 13: Data Bit 6 
# 14: Data Bit 7 
# 15: LCD Backlight +5V 
# 16: LCD Backlight GND

#import 
import RPi.GPIO as GPIO
import time

# Define GPIO to LCD mapping 
LCD_RS = 25
LCD_E = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

#Define GPIO to buttons
BTN1 = 4
BTN2 = 18

#Define some device constants
LCD_FILLER = "--------------------"
LCD_WIDTH = 20
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

E_PULSE = 0.00005
E_DELAY = 0.00005

# Main
#	Will display starting message first
#	Then, depending on which button is pressed, will print out something differenet
def main():

	#Set up pins for GPIO output
    GPIO.setmode(GPIO.BCM)  #Use BCM GPIO numbers
    GPIO.setup(LCD_E,GPIO.OUT)
    GPIO.setup(LCD_RS,GPIO.OUT)
    GPIO.setup(LCD_D4,GPIO.OUT)
    GPIO.setup(LCD_D5,GPIO.OUT)
    GPIO.setup(LCD_D6,GPIO.OUT)
    GPIO.setup(LCD_D7,GPIO.OUT)
	
	#Set up buttons for GPIO input
	GPIO.setup(BTN1, GPIO.IN)
	GPIO.setup(BTN2, GPIO.IN)

	#Initialize LCD Display
    lcd_init()
	
	#Display introductory message
	to_write = [LCD_FILLER, str_format_left("Raspberry Pi"), str_format_left("GPIO Test"), LCD_FILLER]
	lcd_write_lines(to_write)
	time.sleep(5)
	
	#run infinite loop that displays different messages for different button presses
	while True:
		if (GPIO.input(BTN1) == True):
			to_write = [LCD_FILLER, str_format_left("You hit"), str_format_left("Button 1"), LCD_FILLER]
			lcd_write_lines(to_write)
			time.sleep(1)
		if (GPIO.input(BTN2) == True):
			to_write = [LCD_FILLER, str_format_left("You hit"), str_format_left("Button 2"), LCD_FILLER]
			lcd_write_lines(to_write)
			time.sleep(1)

#Function: str_format_left
#	Taking in a string, will return it with enough padding for the LCD display
def str_format_left(s):
	return s = s.ljust(LCD_WIDTH, " ")
	
#Function: lcd_write_lines
#	Takes in a list of 4 strings to be written out to each line in the LCD
def lcd_write_lines(message):
	lcd_byte(LCD_LINE_1,LCD_CMD)
	lcd_string(message[0])
	lcd_byte(LCD_LINE_2,LCD_CMD)
	lcd_string(message[1])
	lcd_byte(LCD_LINE_3,LCD_CMD)
	lcd_string(message[2])
	lcd_byte(LCD_LINE_4,LCD_CMD)
	lcd_string(message[3])

#Function: lcd_init()
#	Initializes LCD display
def lcd_init():
    #init display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)

#Function: lcd_string
#	Will print out to a set line in the LCD display
def lcd_string(message):
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)

#Function: lcd_byte		
#	Send byte to data pins
# 		bits = data
# 		mode = True for character
#        	   False for command
def lcd_byte(bits,mode):

    GPIO.output(LCD_RS,mode)

    #High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x10==0x10:
        GPIO.output(LCD_D4, True)
    if bits&0x20==0x20:
        GPIO.output(LCD_D5, True)
    if bits&0x40==0x40:
        GPIO.output(LCD_D6, True)
    if bits&0x80==0x80:
        GPIO.output(LCD_D7, True)

    #Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

    #Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits&0x01==0x01:
        GPIO.output(LCD_D4, True)
    if bits&0x02==0x02:
        GPIO.output(LCD_D5, True)
    if bits&0x04==0x04:
        GPIO.output(LCD_D6, True)
    if bits&0x08==0x08:
        GPIO.output(LCD_D7, True)

    #Toggle 'Enable' pin
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

#start the program
if __name__ == '__main__':
    main()
