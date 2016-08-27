"""
This server will route requests from twilio (messages sent to phone
number), process them, and sent the appropriate repsonse

https://www.twilio.com/docs/api/twiml/sms/twilio_request
https://www.twilio.com/docs/api/twiml/sms/your_response
"""
"""
example of post data reveived from twilio in within form data:

form ImmutableMultiDict([('FromZip', u'90044'), ('From', u'+13109137479'), 
  ('SmsMessageSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('FromCity', u'LOS ANGELES'), ('ApiVersion', u'2010-04-01'), 
  ('To', u'+14243295324'), ('NumMedia', u'0'), ('NumSegments', u'1'), 
  ('AccountSid', u'AC9a2be4e4c6477d5f1622a68a80694d1a'), 
  ('SmsSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('ToCity', u''), ('FromState', u'CA'), ('FromCountry', u'US'), 
  ('Body', u' Hola bb'), ('MessageSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('SmsStatus', u'received'), ('ToZip', u''), ('ToCountry', u'US'), 
  ('ToState', u'CA')])
"""
from string import digits
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

#this program's files
from creds import credentials
from open_weather_city_lookup import Weather_Data
from database_interactions import DB
from user_interactions import phase0,phase1,phase2,phase3

#import credentials/system specific information
IP = credentials['ip']
PORT = credentials['port']

#xml form to send a response back to twilio as an outgoing message
TWIML_BoilderPlate = '<?xml version="1.0" encoding="UTF-8" ?>' \
  '<Response><Message> MSG_RPLC </Message></Response>'


#create the application
app = Flask(__name__)

#testings
@app.route('/')
def hello_world():
    return '~~ HELLO MY FRIEND ~~'

"""
messages from User to twilio phone are posted
by the twilio server here for the server to decide
on a Response and then the reverse flow occurs

User (txt)-> twilio server (post)-> This Server
This Server (response to post) -> twilio server (txt)-> User
"""

@app.route('/twilio', methods=['post'])
def twilio_message_received():
  #variabes to hold releveant post information
  user_text = request.form['Body']
  user_number = request.form['From']

  #clean up the user number - leading'+'
  user_number = ''.join(c for c in user_number if c in digits)

  #initialize DB
  db = DB()

  #get status of user for routing
  user_status = db.user_signup_phase(user_number)

  msg= '' #to be sent back to user
  
  if user_status == 0:
    msg = phase0(user_number, user_text)

  if user_status == 1:
    msg = phase1(user_number, user_text)
          
  if user_status == 2:  
    msg = phase2(user_number, user_text)

  if user_status == 3: 
    msg = phase3(user_number, user_text)

  #build text response
  twiml_return = TWIML_BoilderPlate.replace('MSG_RPLC', msg)
  return twiml_return


if __name__ == '__main__':
  app.run(host=IP, port = PORT)

