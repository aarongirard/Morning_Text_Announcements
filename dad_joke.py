import random
import re
def build_dad_joke():
  jokes_list = []
  with open('dad_jokes.txt','r') as jokes:
    for joke in jokes:
      jokes_list.append(joke)
    
  #choose randomly from list to get joke of the day
  joke = random.choice(jokes_list)
  
  #need to clean out non alphanumeric cause lazy
  pattern = re.compile('([^\s\w]|_)+')
  joke = re.sub(pattern, '', joke)
  
  return 'Dad joke of the day: ' + joke    
