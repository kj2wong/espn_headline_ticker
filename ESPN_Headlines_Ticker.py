# ESPN Headlines Ticker
#
# This application displays headlines from different sports leagues through the ESPN public API
# Then, using input buttons through the Raspberry Pi's GPIO pins, I can toggle through sports and headlines
# The headline is then displayed on an LCD display, also through the Raspberry Pi's GPIO pins
#
# Author: Kevin Wong
#	With some code from a Raspberry Pi GPIO tutorial from:
#	http://www.youtube.com/watch?v=KM4n2OtwGl0
#
# Date: 11/25/2013

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
import urllib
import json

# Define GPIO to LCD mapping 
LCD_RS = 25
LCD_E = 24
LCD_D4 = 23
LCD_D5 = 17
LCD_D6 = 27
LCD_D7 = 22

#Define GPIO to buttons
BTN1 = 4 #Changes leagues from which to get headlines
BTN2 = 18 #changes the headlines in that league

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

#Define ESPN API constants
API_KEY = "" #insert API key here (will not work if there is no key)
BASE_URL = "http://api.espn.com/v1/sports"

#urls for different sports leagues
URL_DICT = {"NFL" : "/football/nfl",
            "NCAAF" : "/football/college-football",
            "MLB" : "/baseball/mlb",
            "NHL" : "/hockey/nhl",
            "NBA" : "/basketball/nba"}
			
LEAGUE_DICT = {0 : "NFL",
               1 : "NCAAF",
               2 : "MLB",
               3 : "NHL",
               4 : "NBA"}
TOTAL_LEAGUES = 5
			

# Main
#   Will display starting message first
#   Starts off by displaying NFL headlines (default)
#   Then, depending on which button is pressed, will print out something different
#       If the first button is pressed, the league changes (and so do the headlines)
#       If the second button is pressed, the headlines within that league will change
def main():
    league_number = 0
    headline_number = 0
    
    #setup all the hardware
    complete_setup()
	
    #Display introductory message
    to_write = [LCD_FILLER, str_format_center("ESPN"), str_format_center("Headlines Ticker"), LCD_FILLER]
    lcd_write_lines(to_write)
    time.sleep(5)

    #start off with NFL news
    json_data = get_all_headlines_json("NFL")
    headline = json_data["headlines"][0]["headline"]
    format_and_write_output("NFL", str(headline))
    
    while True:
        #if the first button is hit, change leagues, get headlines for league
        #   then, display the first headline for the league
        if (GPIO.input(BTN1) == True):
            league_number = (league_number + 1) % 5
            league_name = LEAGUE_DICT[league_number]
            
            json_data = get_all_headlines_json(league_name)
            headline = json_data["headlines"][0]["headline"]
            
            format_and_write_output(league_name, str(headline))
            headline_number = 0
            time.sleep(1)
            
        #if the second button is hit, just get the next headline for that league    
	    if (GPIO.input(BTN2) == True):
            headline_number = (headline_number + 1) % len(json_data["headlines"])
            
            headline = json_data["headlines"][headline_number]["headline"]
            
            format_and_write_output(LEAGUE_DICT[league_number], str(headline))
            time.sleep(1)


#function: format_and_write_output
#   Given a league and a headline, format it to be displayed on lcd
#   Also, call lcd_write_lines to lcd display
def format_and_write_output(league, headline):
    i = 0

    #split the headline by whitespace
    headline_split = headline.split()
    line2 = ""
    line3 = ""
    line4 = ""
    
    #then see how many words can fit on each line (can only fit 20 char on LCD)
    while i < len(headline_split) and len(line2) + len(headline_split[i]) < LCD_WIDTH:
        line2 += headline_split[i] + " "
        i += 1
        
    while i < len(headline_split) and len(line3) + len(headline_split[i]) < LCD_WIDTH:
        line3 += headline_split[i] + " "
        i += 1
        
    while i < len(headline_split) and len(line4) + len(headline_split[i]) < LCD_WIDTH:
        line4 += headline_split[i] + " "
        i += 1

    #write out to LCD
    to_write = [str_format_center(league),
                str_format_left(line2),
                str_format_left(line3),
                str_format_left(line4),]
    lcd_write_lines(to_write)


#function: get_headlines
#   Pass in a supported league (string) and it returns data in JSON
def get_all_headlines_json(league):
    fetch_url = BASE_URL + URL_DICT[league] + "/news/headlines?apikey=" + API_KEY
    data = urllib.urlopen(fetch_url)
    return json.loads(str(data.read()))

			
#Function gpio_setup
#   Sets up all the pins for the GPIO
#   Calls lcd_init as well
def complete_setup():
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

			
#Function: str_format_left
#   Taking in a string, will return it with enough padding for the LCD display
def str_format_left(s):
    return s.ljust(LCD_WIDTH, " ")


#Function: str_format_header
#   Taking in a string, will return it centered
def str_format_center(s):
    return s.center(LCD_WIDTH, "-")

	
#Function: lcd_write_lines
#   Takes in a list of 4 strings to be written out to each line in the LCD
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
#   Initializes LCD display
def lcd_init():
    #init display
    lcd_byte(0x33,LCD_CMD)
    lcd_byte(0x32,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x06,LCD_CMD)
    lcd_byte(0x01,LCD_CMD)


#Function: lcd_string
#   Will print out to a set line in the LCD display
def lcd_string(message):
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)


#Function: lcd_byte		
#   Send byte to data pins
# 	bits = data
# 	mode = True for character
#              False for command
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
