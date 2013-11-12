# ESPN Headlines
#   Author: Kevin Jordan Wong
#   Purpose: Using the public ESPN API, grab headlines for different sports
#   Note: this is a starting point for the code necessary to operate the GPIO pins of a Raspberry Pi

import urllib
import json
import time

#constants
API_KEY = "" #insert API_KEY here
BASE_URL = "http://api.espn.com/v1/sports"

URL_DICT = {"NFL" : "/football/nfl",
            "NCAAF" : "/football/college-football",
            "MLB" : "/baseball/mlb",
            "NHL" : "/hockey/nhl",
            "NBA" : "/basketball/nba"}

#function: get_headlines
#   Pass in a supported league (string) and it returns data in JSON
def get_headlines(league):
    fetch_url = BASE_URL + URL_DICT[league] + "/news/headlines?apikey=" + API_KEY
    data = urllib.urlopen(fetch_url)
    return json.loads(str(data.read()))

#function: print_headlines
#   Hardcoded to infinitely loop through headlines and print them to console at 5s intervals.
#   Refreshes headlines after each time through the list of headlines
def print_headlines(league):
    json_data = get_headlines(league)
    i = 0

    while True:
        print json_data["headlines"][i]["headline"]
        time.sleep(5)
        i += 1
        if i == len(json_data["headlines"]):
            json_data = get_headlines(league)
            i = 0

#Start code
print_headlines("NFL")
