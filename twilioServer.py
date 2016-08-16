from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash


#create the application
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'YOU ARE IN AARONS DOMAIN MOOOAHAHAH'

if __name__ == '__main__':
  app.run(host="104.236.230.232", port = 5000)
