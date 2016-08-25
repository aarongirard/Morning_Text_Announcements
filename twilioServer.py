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


import sqlite3 as sql
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash
from creds import credentials

DBNAME = credentials['dbname']
IP = credentials['ip']
PORT = credentials['port']

#xml form to send a response back to twilio as an outgoing message
TWIML_BoilderPlate = '<?xml version="1.0" encoding="UTF-8" ?> \
  <Response><Message> MSG_RPLC </Message></Response>'


#create the application
app = Flask(__name__)

"""
check whether a user is in DB, if yes, return signup phase #
rtn values: meaning
0: not in system
1: has been asked to join / for users location
2: has been asked to chose between locations
3: already signed up
"""
def user_signup_phase(user_phonenumber):
  results = ''
  with sql.connect(DBNAME) as connection:
    c = connection.cursor()
    c.execute('select * from users where phonenumber = '+str(user_phonenumber)+';')
    results = c.fetchall()
  if results:
    return results[0][3]
  else:
    return 0

#testings
@app.route('/')
def hello_world():
    print user_signup_phase(3109137479)
    print 'Aasaddsfasfd'
    print user_signup_phase(3109137449)
    return 'HI'

"""
messages sent back to twilio phone are posted
by the twilio server here for the server to decide
on a Response

"""

@app.route('/twilio', methods=['post'])
def twilio_message_received():
  user_text = request.form['Body']
  user_number = request.form['From']

  #clean up the user number - leading'+'
  if '+' in user_number:
    user_number = user_number[1:]
  
  #get status of user 
  user_status = user_signup_phase(user_number)

  msg= '' #to be sent back to user
  
  """
  user not in system:
  1. ask if they would like to join
    a. if not response with 'No'
    b.If yes, respond with ask for the city where they 
    would like to recevie weather data for
    -could implement the city given in text metadata?
  """  
  if user_status == 0:
    msg = 'Hey you, would you like to sign up for Morning anouncemnts? \
    If so please respond with the city for which you would like weather\
    anouncements. If not, just respond with \'No\'.'

    #create record in DB 

  """
  1. If the response is 'No', then respond with condolence msg
  and deltete their record from the DB
  2. If the response is not 'No'
    a. look up users given location.
      i. send results back to them if more than one loc found
      and ask to respond with the corresponding number of the 
      correct location. Set code to 2
      ii. if one loc found, use this city ID and respond with
      message detailing that they have been signed up for given 
      loc and set code to 3
  """ 
  if user_status == 1:
    #convert string to array to check for word No
    text = user_text.lower().split()
    if 'no' in text:
      msg = 'I\'m sorry to hear that. If you change your mind \
      I\'m here waitng'

      #delete record from DB

      continue

    else: 
      location = user_text 

  """
  1. set their record to the corresponding loc they responded with
  and set code to 3
  """
  if user_status == 2:  
  

  if user_status == 3: 
    msg = 'Silly, you\'ve already signed up for service'



  #build text response
  twiml_return = TWIML_BoilderPlate.replace('MSG_RPLC', msg)
  return twiml_return


if __name__ == '__main__':
  app.run(host=IP, port = PORT)

