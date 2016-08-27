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

  #initialize DB
  db = DB()

  #clean up the user number - leading'+'
  user_number = ''.join(c for c in user_number if c in digits) 
  
  #get status of user 
  user_status = db.user_signup_phase(user_number)

  msg= '' #to be sent back to user
  
  """
  (0)user not in system:
  1. ask if they would like to join
    a. if not they should respond with 'No'
    b.If yes, respond with ask for the city where they 
    would like to recevie weather data for
    -could implement the city given in text metadata?
  """  
  if user_status == 0:
    msg = 'Hey you, would you like to sign up for Morning anouncemnts? ' \
    'If so please respond with the city for which you would like weather ' \
    'anouncements. If not, just respond with \'No\'.'

    #create record in DB, set status_phase as 1
    db.add_user_record(phonenumber, signupphase = 1)

  """
  (1)
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
    
    #user does not want to sign up
    if 'no' in text:
      msg = 'I\'m sorry to hear that. If you change your mind ' \
      'I\'ll be here waitng'

      #delete record from DB
      db.delete_user_record(int(user_number))
    else: 
      #find location in open_weather data 
      location = user_text
      wd = Weather_Data()

      #(city name, state name, ID), all strings
      possible_cities = wd.get_locations_by_city(location)
      
      #if empty, then location not valid; keep phase at 1
      if not possible_cities:
        msg = 'I couldn\'t use that location. make sure to send me ' \
        'only the city name'
      else:
        #if length one, then use this city; phase = 3
        if len(possible_cities) == 1:
          db.update_user_record(int(user_number),possible_cities[0][2],\
            possible_cities[0][0] + ', ' + possible_cities[0][1], 3)
          
          #respond telling user they have been signed up to x city
          msg = 'You have been signed up for weather alerts for ' \
            + possible_cities[0][0] + ', ' + possible_cities[0][1]
        else: 
          #cache possible locations with order
          #repsonse , asking for which number
          #set phase to 2
          
  """
  (2)
  1. set their record to the corresponding loc they responded with
  and set code to 3
  """
  if user_status == 2:  
    pass

  """
  (3)
  """
  if user_status == 3: 
    #if contains cancel
    #else below msg

    msg = 'Silly, you\'ve already signed up for service. To cancel ' \
    'message me \'cancel\''



  #build text response
  twiml_return = TWIML_BoilderPlate.replace('MSG_RPLC', msg)
  return twiml_return


if __name__ == '__main__':
  app.run(host=IP, port = PORT)

