import datetime
def log(thing_to_log):
  with open('log.txt', 'a+') as f:
    f.write(str(datetime.datetime.now())+',  ' + str(thing_to_log) + '\n')