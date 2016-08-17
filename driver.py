import requests
import json
import datetime
import time
import sqlite3 as sql

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

DB schema:
table: users
 phonenumber text, cityid text, cityname text, signupphase integer
"""
#PHONE_NUMBERS = credentials['phone_numbers'] depreciated
DBNAME = credentials['dbname']
TWILIO_FROM_NUMBER = credentials['twilio_phone_number']
TWILIO_SID = credentials['twilio_sid']
TWILIO_AUTH_TOKEN = credentials['auth_token']

#creates tables for app. only need to do once or else might overwrite data...
def create_tables(): 
  #should automatically close connection after execution
  with sql.connect(DBNAME) as connection:
    c = connection.cursor()
    #for gps: gps(Time TEXT,Lat TEXT,Long TEXT,Speed TEXT)
    c.execute('CREATE TABLE users(phonenumber INTEGER PRIMARY KEY,\
      cityid TEXT NOT NULL,cityname \
      TEXT NOT NULL,signupphase INTEGER NOT NULL)')
    connection.commit() #commit insertion to DB

#add records without doing twilio process
def add_existing_records(phonenumber = 000000000, cityid = 'Null', 
  cityname = 'Null', signupphase = 1):
  with sql.connect(DBNAME) as connection:
    c = connection.cursor()
    values = (phonenumber,cityid,cityname,signupphase)
    c.execute('INSERT INTO users(phonenumber,cityid,cityname,signupphase) \
      VALUES (?,?,?,?)', values)

def fetch_all_records():
  with sql.connect(DBNAME) as connection:
    c = connection.cursor()
    c.execute('Select * from users') #need semicolon?
    records = c.fetchall() #iterable DS of tuples
    return records #(tuple for each record)

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
      #for num in PHONE_NUMBERS: depreciated
      records = fetch_all_records()
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
