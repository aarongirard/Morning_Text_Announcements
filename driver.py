import requests
import json
import datetime
import time
import sqlite3 as sql

from twilio.rest import TwilioRestClient
from message import build_weather
from dad_joke import build_dad_joke
from creds import credentials
from database_interactions import DB

"""
Need creds.py file with

phone_numbers = [of numbers]

credentials = {'city_ID', 'APPID'}
city_ID = id of city wrt open weather
appid = api id from open weather

DB schema:
table: users
 phonenumber text, cityid text, cityname text, signupphase integer
"""
#PHONE_NUMBERS = credentials['phone_numbers'] depreciated
TWILIO_FROM_NUMBER = credentials['twilio_phone_number']
TWILIO_SID = credentials['twilio_sid']
TWILIO_AUTH_TOKEN = credentials['auth_token']

#method to send to someone who has joined the service
def initial_msg(number):
  msg = 'You\'ve signed up for morning anouncements!'
  
  client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
  message = client.messages.create(body=msg,to=number,
    from_=TWILIO_FROM_NUMBER)
  #post = requests.post('http://textbelt.com/text',
    #data = {'number': number, 'message': msg})

def main():
  while True:
    #run at some time at 6:xx am
    if datetime.datetime.now().hour == 6:
      #get todays dad joke of the day
      todays_dad_joke = build_dad_joke()
      
      #query database for all records
      db = DB()
      records = db.fetch_all_user_records()

      #send message to each signed up record
      for record in records:
        if record[3] !=3:
          print str(record[0]) +' is not fully signed up' 
          continue
        msg = build_weather(record[1]) #num[1] is city id
        msg  += '  ' + todays_dad_joke
        
        #send twilio messages
        client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=msg,to=record[0],
          from_=TWILIO_FROM_NUMBER)

        #url, data{}, message using textbelt.com
        #post = requests.post('http://textbelt.com/text',
        #data = {'number': num, 'message':message})
        print 'sent ' + str(record[0]) + ' at ' +  str(datetime.datetime.now().hour)
    time.sleep(3600) #sleep for 60mins

#response
#print post.text

#run this if run from commnand line, and not import
if __name__ == "__main__":
  main()
  #don't run anythin on import
