# Morning_Text_Announcements#
Send morning text announcements by text to a list of phone numbers and brighten your friends day

To implement, run these two files (python x.py &) on your server:

-user_interaction_server: chat bot to interact with user (signing up, etc)

-distribution.py: script that distributes text every morning between 6-7am

-set up a sms phone number on twilio; point it towards the ip and port specified below

-create a creds.py file with a dictionary called credentials with the following keys:
  credentials = {
    'twilio_phone_number': '',
    'twilio_sid' : '',
    'dbname' : 'morning_anouncements.db',
    'wunderground_api': '',
    'ip' :'', #of your server
    'port' :
  }

-intialize the db table using the respective method in database_interactions.py

To add more to the message, write a script in a different file, import a function into driver.py that returns the
desired info as a string and place it in the for loop / concatentate its contents with msg!
