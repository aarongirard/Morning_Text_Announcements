import requests
import json
import datetime
import time
from twilio.rest import TwilioRestClient
from message import build_weather
from dad_joke import build_dad_joke
from creds import credentials

"""
Need creds.py file with

phone_numbers = [of numbers]

credentials = {'city_ID', 'APPID'}
city_ID = id of city wrt open weather
appid = api id from open weather
"""
PHONE_NUMBERS = credentials['phone_numbers']
TWILIO_FROM_NUMBER = credentials['twilio_phone_number']
TWILIO_SID = credentials['twilio_sid']
TWILIO_AUTH_TOKEN = credentials['auth_token']

def initial_msg(number):
  client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
  msg = 'You\'ve signed up for morning anouncements!'
  message = client.messages.create(body=msg,to=number,
    from_=TWILIO_FROM_NUMBER)
  #post = requests.post('http://textbelt.com/text',
    #data = {'number': number, 'message': msg})

def main():
  while True:
    #run at some time at 6:xx am
    if datetime.datetime.now().hour == 6:
      message = build_weather()
      message+= '  ' + build_dad_joke()
      for num in PHONE_NUMBERS:
        message = client.messages.create(body=message,to=num,
          from_=TWILIO_FROM_NUMBER)
        #url, data{}
        #post = requests.post('http://textbelt.com/text',
         #data = {'number': num, 'message':message})
        print 'sent ' + str(num) + ' at ' +  str(datetime.datetime.now().hour)
    time.sleep(3600) #sleep for 60mins

#response
#print post.text

#run this if run from commnand line, and not import
if __name__ == "__main__":
  main()
  #don't run anythin on import
