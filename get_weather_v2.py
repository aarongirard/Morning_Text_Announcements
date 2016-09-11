import requests
import json
import datetime
from creds import credentials

#apis
APPID = credentials['wunderground_api']#credentials['open_weather_key']


def get_weather_from_api(zipcode):
  ZIPCODE = zipcode
  
  url = 'http://api.wunderground.com/api/{APPID_}/hourly/q/{ZIPCODE_}.json'
  print url
  url = url.format(APPID_ = APPID,ZIPCODE_ = ZIPCODE)
  print url
  #send request for Atl weather data to get current temp
  weather = requests.get(url)

  #convert reponse to json object
  weather_data = json.loads(weather.text)
  forecasts = weather_data['hourly_forecast']
  today = datetime.datetime.now().day

  hourly_weather = {} #holds dictionary {24hrtime: temp in F}
  for forecast in forecasts:
    #if forcast is for today
    if int(forecast['FCTTIME']['mday_padded']) == today:
      #forecast['FCTTIME']['weekday_name_unlang'] 
      hourly_weather[int(forecast['FCTTIME']['hour'])] = int(forecast['temp']['english'])
  return hourly_weather

def build_weather(zipcode):
  #boilerplate for message
  #add functionality to suggest dress wear for different weathers
  msg = 'The average temperature today is '\
    '{AVGTEMP} with a high of {HIGHTEMP} at {TIMEHIGHTEMP}'

  #get weather data
  weather = get_weather_from_api(zipcode)

  AVGTEMP_ = 0
  HIGHTEMP_ = 0 
  TIMEHIGHTEMP_ = 0

  #calculate metrics for msg
  for time,temp in weather.iteritems():
    AVGTEMP_+= temp
    if temp > HIGHTEMP_:
      HIGHTEMP_ = temp
      TIMEHIGHTEMP_ = time

  AVGTEMP_ /= len(weather)

  if TIMEHIGHTEMP_ <= 12: 
    TIMEHIGHTEMP_ = str(TIMEHIGHTEMP_) + ' a.m.'  
  else:
    TIMEHIGHTEMP_ = str(TIMEHIGHTEMP_%12) + ' p.m.' 

  msg = msg.format(AVGTEMP=AVGTEMP_,HIGHTEMP=HIGHTEMP_,
    TIMEHIGHTEMP=TIMEHIGHTEMP_)
  return msg





  