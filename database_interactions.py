"""
API for interacting with database
Refactored out these methods because it was getting crazy
to have them in one file
 - learning some stuffs
"""

import sqlite3 as sql
from creds import credentials

#name of database to interact with
#can be hard coded into this file b.c. project uses
#only one db
DBNAME = credentials['dbname']

class DB: 
  def __init__(self):
    self.DBNAME = DBNAME

  ###functions for interacting with user table###
  def add_user_record(self, phonenumber = 0000000000, cityid = 'Null', 
    cityname = 'Null', signupphase = 0):
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      values = (phonenumber,cityid,cityname,signupphase)
      c.execute('INSERT INTO users(phonenumber,cityid,cityname,signupphase)' \
        'VALUES (?,?,?,?)', values)

  #this needs to be tested   
  #phonenumber = int 
  def delete_user_record(self, phonenumber):
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      c.execute('Delete from users where phonenumber=?', (phonenumber,))

  def update_user_record(self, phonenumber, cityid, cityname, signupphase):
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      c.execute('Update users set cityid=?, cityname=?, signupphase=?' \
        'where phonenumber=?', (cityid, cityname, signupphase, phonenumber))

  """
  check whether a user is in DB, if yes, return signup phase #
  rtn values: meaning
  0: not in system
  1: has been asked to join / for users location
  2: has been asked to chose between locations
  3: already signed up
  """
  def user_signup_phase(self, user_phonenumber):
    results = ''
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      c.execute('select * from users where phonenumber = '+str(user_phonenumber)+';')
      results = c.fetchall()
    
    #if in system, return value, if not return 0
    if results:
      return results[0][3]
    else:
      return 0 

  #fetches all records in database, returns them
  def fetch_all_user_records(self):
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      c.execute('Select * from users') #need semicolon?
      records = c.fetchall() #iterable DS of tuples
      return records #(tuple for each record)

  ####FUNCTIONS WITH INTERACTING WITH WEAHTER_LOOKUP CACHE TABLE###

  #creates tables for app. only need to do once or else might overwrite data...
  #module private
  def _create_user_table(self): 
    #should automatically close connection after execution
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      #for gps: gps(Time TEXT,Lat TEXT,Long TEXT,Speed TEXT)
      c.execute('CREATE TABLE users(phonenumber INTEGER PRIMARY KEY, ' \
        'cityid TEXT NOT NULL,cityname ' \
        'TEXT NOT NULL,signupphase INTEGER NOT NULL)')
      connection.commit() #commit insertion to DB

  #table to hold the possible locations between phase 2 and 3
  def _create_location_choice_cache_table(self): 
    with sql.connect(DBNAME) as connection:
      c = connection.cursor()
      #for gps: gps(Time TEXT,Lat TEXT,Long TEXT,Speed TEXT)
      c.execute('CREATE TABLE LocationChoiceCache(phonenumber INTEGER ' \
        'PRIMARY KEY, cityid TEXT NOT NULL,cityname ' \
        'TEXT NOT NULL,signupphase INTEGER NOT NULL)')
      connection.commit() #commit insertion to DB

  ####FUNCTIONS WITH INTERACTING WITH WEAHTER_LOOKUP CACHE TABLE###


def main():
  pass

if __name__ == "__main__":
  main()








