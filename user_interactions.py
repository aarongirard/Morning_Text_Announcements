#ROUTES for USER interaction base on SIGNUP PHASE
from database_interactions import DB

###FUNCTIONS FOR RESPONDING TO EACH PHASE###
#number will always be an int
#text will always be a string

"""
(0)
user not in system:
1. ask if they would like to join
  a. if not they should respond with 'No'
  b.If yes, respond with ask for the city where they 
  would like to recevie weather data for
  -could implement the city given in text metadata?
"""  
def phase0(number, text):
    db = DB()
    msg = 'Hey you, would you like to sign up for Morning anouncemnts? ' \
    'If so please respond with the zipcode for where you would like weather ' \
    'anouncements. If not, just respond with \'No\'.'

    #create record in DB, set status_phase as 1
    db.add_user_record(number, signupphase = 1)

    return msg

"""
(1)
1. If the response is 'No', then respond with condolence msg
and deltete their record from the DB
2. If the response is not 'No'
  a. check if zipcode is valid (naive implemenation)
    i. if not valid, then reask for zipcode
    ii. if valid sign them up with this zipcode
""" 
def phase1(number, text):
  db = DB()
  msg = ''

  #convert string to array to check for word No
  user_text = text.lower().split()
  
  #user does not want to sign up
  if 'no' in user_text:
    msg = 'I\'m sorry to hear that. If you change your mind ' \
    'I\'ll be here waitng'

    #delete record from DB
    db.delete_user_record(number)
    return msg
  
  zipcode = text
  if len(text) != 5:
    msg = 'Your zipcode does not seem to be valid. please'\
      ' send me just your 5 digit zipcode only.'

    #db.update_user_phase(number,2)
    return msg

  try:
    zipcode = int(text)
  except ValueError: 
    #ask for valid zip
    msg = 'Your zipcode does not seem to be valid. please'\
      ' send me just your 5 digit zipcode only.'
    #db.update_user_phase(number,2)
    return msg


  #respond telling user they have been signed up to x city
  msg = 'You have been signed up for weather alerts for ' \
    + str(zipcode) + '. Please respond with \'change zipcode\''\
    ' to change your set location'
  db.update_user_record(number,zipcode,3)
  return msg
  
"""
(2)
1. used for changing a zipcode
"""

def phase2(number, text):
  db = DB()
  msg = ''

  zipcode = text
  if len(text) != 5:
    msg = 'Your zipcode does not seem to be valid. please'\
      ' send me just your 5 digit zipcode only.'
    return msg

  try:
    zipcode = int(text)
  except ValueError: 
    #ask for valid zip
    msg = 'Your zipcode does not seem to be valid. please'\
      ' send me just your 5 digit zipcode only.'
    return msg

  #respond telling user they have been signed up to x zipcode
  msg = 'You have been signed up for weather alerts for ' \
    + str(zipcode) + '.'
  db.update_user_record(number,zipcode,3)
  return msg



"""
(3)
User already signed up
Handling canceling here
"""
def phase3(number, text):
  db = DB()
  msg = ''
  if 'cancel please' in text.lower():
    db.delete_user_record(number)
    msg = 'Your subscription has been terminated /cry'
    return msg

  if 'change zipcode' in text.lower():
    msg= 'Please send me your new zipcode. ie. \'90272\''
    db.update_user_record(number,0,2)
    return msg
  
  #else  
  msg = 'Silly, you\'ve already signed up for service. To cancel ' \
    'message me \'cancel please\''
  return msg



