import requests
import json
import datetime
from creds import credentials

#apis
APPID = credentials['open_weather_key']
CITY_ID = credentials['city_ID']

#convert Kelvin to F
def convert_K_F(kelvin):
  return kelvin * 1.8 - 459.67

def get_weather():
  #send request for Atl weather data to get current temp
  weather = requests.get('http://api.openweathermap.org/data/2.5/weather',
    params={'id': CITY_ID, 'APPID': APPID})

  #convert reponse to json object
  weather_data = json.loads(weather.text)

  #take weather data from json object, conver to farenheit
  current_temp = convert_K_F(float(weather_data['main']['temp']))

  #send request ATL for weather forecast
  #this gets the 5day forcast every 3 hrs
  #parse it to only get todays data 
  weather_f = requests.get('http://api.openweathermap.org/data/2.5/forecast',
    params={'id': CITY_ID, 'APPID': APPID})

  forecast = json.loads(weather_f.text)

  #set up variables
  min_tmp = 1000.0
  max_tmp = -1000.0
  rain = False


  #list of dictionaries of 3hr forcasts
  forecasts = forecast['list']
  for fc in forecasts:
    #break if next day (don't want that data)
    d1 = datetime.datetime.now().day
    d2 = int(fc['dt_txt'][8:10])
    if d2 != d1:
      break
    #get min/max temps; check if they are greater 
    tmp_min_temp = convert_K_F(float(fc['main']['temp_min']))
    if tmp_min_temp < min_tmp:
      min_tmp = tmp_min_temp
    tmp_max_temp = convert_K_F(float(fc['main']['temp_max']))
    if tmp_max_temp > max_tmp:
      max_tmp = tmp_max_temp
    #check if it is going to rain
    #ie.e do any of the 3hr forecasts have non empty rain dict
    try:
      if fc['rain']:
        rain = True
    except KeyError, e:
      continue #sometimes rain not in dict

  return {'cur_tmp': str(int(current_temp)), 'min_tmp': str(int(min_tmp)), 
    'max_tmp': str(int(max_tmp)), 'rain': rain}

def build_message():
  msg = '' 
  
  #get weather data
  weather = get_weather()

  msg += 'The current weather is ' + weather['cur_tmp'] + '. Dress for anything between '\
    + weather['min_tmp'] + '-' + weather['max_tmp'] + '.'
  if weather['rain']:
    msg+= ' It might rain =('

  return msg




  