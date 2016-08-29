#ROUTES for USER interaction base on SIGNUP PHASE

from open_weather_city_lookup import Weather_Data
from database_interactions import DB

###UTILITY FUNCTIONS###

def check_for_word(text, word):
  text = text.lower().split()
  word = word.lower()
  if word in text:
    return True
  else:
   return False

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
    'If so please respond with the city for which you would like weather ' \
    'anouncements. If not, just respond with \'No\'.'

    #create record in DB, set status_phase as 1
    db.add_user_record(number, signupphase = 1)

    return msg

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
  else: 
    #user wants to sign up, find location in open_weather data 
    location = text
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
        db.update_user_record(number,possible_cities[0][2],\
          possible_cities[0][0] + ', ' + possible_cities[0][1], 3)
        
        #respond telling user they have been signed up to x city
        msg = 'You have been signed up for weather alerts for ' \
          + possible_cities[0][0] + ', ' + possible_cities[0][1]
      else: 
        #cache possible locations with order
        #repsonse , asking for which number
        #set phase to 2

       
        msg = 'Please respond with the number corresponding with the correct ' \
        'location such as \'1\', Here they are: \n'
        for index,city in enumerate(possible_cities):
          #varibales for clarity
          cityname = city[0]
          statename = city[1]
          stateID = city[2]
          ordernum = index+1
          
          db.add_location_cache(number, stateID, cityname, statename, ordernum)
          
          msg += str(index+1) + '.' + cityname +', ' + statename + '\n'
      #set phase =2
      db.update_user_phase(number,2)
  return msg

"""
(2)
1. set their record to the corresponding loc they responded with
and set code to 3
"""
def phase2(number, text):
  db = DB()
  msg = ''

  #text must be an integer
  try:
    loc = int(text)
  except ValueError:
    msg = 'please respond with only the number corresponding ' \
      'to your location'
    return msg
  
  #get cached location
  user_location = db.get_location_cache(number,loc)
  print user_location
  
  #if loc empty, then not valid input
  if not user_location:
    msg = 'please respond with only the number corresponding ' \
      'to the location'
    return msg
  
  #looks valid, set user location in DB; respond with success
  #set phase = 3
  cityid = user_location[0][1]
  cityname = user_location[0][2]
  signupphase = 3
  db.update_user_record(number, cityid, cityname, signupphase)
  db.delete_location_caches(number)
  msg = 'You\'ve been signed up for morning anouncements!'

  return msg

"""
(3)
User already signed up
Handling canceling here
"""
def phase3(number, text):
  msg = ''
  if check_for_word(text, 'cancel'):
    db = DB()
    db.delete_user_record(number)
    msg = 'Your subscription has been terminated /cry'
  else: 
    msg = 'Silly, you\'ve already signed up for service. To cancel ' \
      'message me \'cancel\''
  return msg


