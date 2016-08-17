"""
This server will route requests from twilio (messages sent to phone
number), process them, and sent the appropriate repsonse

https://www.twilio.com/docs/api/twiml/sms/twilio_request
https://www.twilio.com/docs/api/twiml/sms/your_response
"""

from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash


#create the application
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'YOU ARE IN AARONS DOMAIN MOOOAHAHAH'

@app.route('/twilio', methods=['post'])
def twilio_message_received():
  print request.form['Body']
  return '<?xml version="1.0" encoding="UTF-8" ?><Response><Message>Hey BB</Message></Response>'
"""
example of information reveived from twilio in post within form data:

form ImmutableMultiDict([('FromZip', u'90044'), ('From', u'+13109137479'), 
  ('SmsMessageSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('FromCity', u'LOS ANGELES'), ('ApiVersion', u'2010-04-01'), 
  ('To', u'+14243295324'), ('NumMedia', u'0'), ('NumSegments', u'1'), 
  ('AccountSid', u'AC9a2be4e4c6477d5f1622a68a80694d1a'), 
  ('SmsSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('ToCity', u''), ('FromState', u'CA'), ('FromCountry', u'US'), 
  ('Body', u' Hola bb'), ('MessageSid', u'SM39420222d885296e1af509f9c59d7776'), 
  ('SmsStatus', u'received'), ('ToZip', u''), ('ToCountry', u'US'), 
  ('ToState', u'CA')])
"""

if __name__ == '__main__':
  app.run(host="104.236.230.232", port = 5000)
