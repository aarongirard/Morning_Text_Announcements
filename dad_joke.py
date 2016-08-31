import random
import re

def build_dad_joke():
  dad_joke_history = set()
  #read in dad joke history
  try:
    with open('dad_joke_history.txt', 'r') as f:
      for line in f:
        dad_joke_history.add(int(line))
  except IOError:
    pass #prob first time running program, no history yet

  print 'history: ', dad_joke_history

  jokes_list = []
  with open('dad_jokes.txt','r') as jokes:
    for joke in jokes:
      jokes_list.append(joke)
    
  #choose randomly from list to get joke of the day
  #joke = random.choice(jokes_list) depreciated, need index for history
  choice = random.randint(0,len(jokes_list)-1) #a<=N<=b
  
  #resample if already used
  while choice in dad_joke_history:
    print'need to resample: ', choice
    choice = random.randint(0,len(jokes_list)-1)

  print 'choice: ', choice
  #add choice to dad joke history
  with open('dad_joke_history.txt', 'a+') as f:
    f.write(str(choice) + '\n')
    print 'wrote choice to history'
  joke = jokes_list[choice]
  
  #need to clean out non alphanumeric cause lazy
  pattern = re.compile('([^\s\w]|_)+')
  joke = re.sub(pattern, '', joke)
  
  return 'Dad joke of the day: ' + joke    

#for testing
def main():
  from dad_joke import build_dad_joke
  build_dad_joke()

if __name__ == '__main__':
  main()

