"""
class to help parse open weather city city ID's for users
 - file only contains city names so need to geolocate the state
 because many cities are ambiguous i.e. Durham
"""

import ast
import urllib2 as url

GOOGLE_API_KEY = 'AIzaSyBYHNQc8rMXxUnQ9ZTVNQPuVQG5MkXjaPQ'


class Weather_Data:
  #playing around with setting up debug code that can be 
  #easily turned on and off
  DEBUG = False
  @staticmethod
  def debug(string):
    if Weather_Data.DEBUG:
      print string
  
  #on initialization, load city data
  def __init__(self):
    self.list_of_city_data = []
    with open('open_weather_city_list.json', 'r') as f:
      [self.list_of_city_data.append(ast.literal_eval(line)) for line in f]
  
  """
  weather data only contains city name, need to find state b.c of like names
  the @staticmethod declarations tells python not to send the 'self' variable
  when the method is called on an isntance and not on the class 
  http://stackoverflow.com/questions/735975/static-methods-in-python
  """
  @staticmethod
  def get_state_from_latlng(lat,long,api_key):
    #request reverse geocode of given data from googlemaps api
    req_string = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=LAT_RPLC,LONG_RPLC&key=API_KEY_RPLC'\
      .replace('LAT_RPLC',lat).replace('LONG_RPLC',long).replace('API_KEY_RPLC', api_key)
    Weather_Data.debug(req_string)
    req = url.Request(req_string)
    try:
      resp = url.urlopen(req)
    except url.URLError as e:
      print str(e.reason)
      return 0
    return resp.read()
  
  #method to parse response from le googs
  @staticmethod
  def parse_reverse_geocode_response(response):
    #parse response for state
    state_name = ''
    response = ast.literal_eval(response)['results'][0]["address_components"]  

    #admin lvl 1 = state level
    for address_components in response:
      if 'administrative_area_level_1' in address_components['types']:
        state_name = address_components['long_name']
        break
      #if no state found, empty string signifies this
    return state_name 

  #find cities that contain the user provided city name
  #returns tuple of strings (city name, state, cityid)
  def get_locations_by_city(self, city):
    #find cities that could correspond to user input
    possible_cities = []
    for city_ in self.list_of_city_data:
      print city
      print city_['name']
      if city.lower() in city_['name'].lower():
        possible_cities.append(city_)
    
    Weather_Data.debug(possible_cities)

    #geolocate each city to get state
    city_state_tuples = [] 
    
    #reverse geolocate state from lat/long
    for city_ in possible_cities:  
      content = Weather_Data.get_state_from_latlng(str(city_['coord']['lat']),\
        str(city_['coord']['lon']),GOOGLE_API_KEY)
      
      #empty if no state found, but should not be encountered
      state_name = Weather_Data.parse_reverse_geocode_response(content)    
      
      Weather_Data.debug(state_name)
      city_state_tuples.append((str(city_['name']),state_name, str(city_['_id'])))
    
    Weather_Data.debug(city_state_tuples)
    return city_state_tuples
  
  
    
#get_state_from_latlng(lat,lon,GOOGLE_API_KEY)
{'country': 'US', '_id': 5368381, 'name': 'Los Angeles County', 'coord': {'lat': 34.366661, 'lon': -118.200912}}

#from open_weather_city_lookup import Weather_Data
#wc = Weather_Data()
#wc.get_locations_by_city('Los Angeles')

