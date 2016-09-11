import requests
import json
import datetime
import time
import sqlite3 as sql

from twilio.rest import TwilioRestClient
from get_weather_v2 import build_weather
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

def adhoc_msg(msg):
  #query database for all records
  db = DB()
  records = db.fetch_all_user_records()

  for record in records:
    if record[2] !=3:
      continue
    #send twilio messages
    client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=msg,to=record[0],
      from_=TWILIO_FROM_NUMBER)

def main():
  while True:
    #run at some time at 6:xx am
    if datetime.datetime.now().hour == datetime.datetime.now().hour:
      #get todays dad joke of the day
      todays_dad_joke = build_dad_joke()
      
      #query database for all records
      db = DB()
      records = db.fetch_all_user_records()

      #send message to each signed up record
      #wait 1 minute every 10 records b.c of api limit =(
      apisent = 0
      for record in records:
        if record[2] !=3:
          print str(record[0]) +' is not fully signed up' 
          continue
        msg = build_weather(record[1]) #zipcode
        msg  += '  ' + todays_dad_joke
        
        #send twilio messages
        client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(body=msg,to=record[0],
          from_=TWILIO_FROM_NUMBER)
        
        apisent+=1
        if apisent%10 == 0:
          time.sleep(60)

        print 'sent ' + str(record[0]) + ' at ' +  str(datetime.datetime.now().hour)
    time.sleep(3600) #sleep for 60mins

if __name__ == "__main__":
  main()

