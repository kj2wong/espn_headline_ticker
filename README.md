espn_headline_ticker
====================

This application displays headlines from different sports leagues through the ESPN public API
Then, using input buttons through the Raspberry Pi's GPIO pins, I can toggle through sports and headlines
The headline is then displayed on an LCD display, also through the Raspberry Pi's GPIO pins


There are 3 files in this repo

1) TEST_headlines_only.py 
    - simply grabs headlines through the API and cycles through them in timed intervals
    
2) TEST_gpio_only.py 
    - is a program to test the input and output of the Raspberry Pi GPIO pins
    
3) ESPN_Headlines_Ticker.py
    - this script is the actual application which uses buttons to grab headlines from the API and display them on the LCD
