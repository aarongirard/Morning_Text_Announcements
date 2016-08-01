import requests
import json
import datetime
import time
from message import build_message
from creds import phone_numbers

"""
Need creds.py file with

phone_numbers = [of numbers]

credentials = {'city_ID', 'APPID'}
city_ID = id of city wrt open weather
appid = api id from open weather
"""

def initial_msg(number):
  msg = 'You\'ve signed up for morning anouncements!'
  post = requests.post('http://textbelt.com/text',
    data = {'number': number, 'message': msg})

def main():
  while True:
    #run at some time at 6:xx am
    if datetime.datetime.now().hour == 6:
      message = build_message()
      for num in phone_numbers:
        #url, data{}
        post = requests.post('http://textbelt.com/text',
         data = {'number': num, 'message':message}
        )
        print 'sent ' + num + ' at ' +  datetime.datetime.now().hour
    time.sleep(3600) #sleep for 60mins

#response
#print post.text

#run this if run from commnand line, and not import
if __name__ == "__main__":
  main()
  #don't run anythin on import
