__author__ = 'zainul'
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.mail import Mail, Message
import os

app = Flask(__name__)
# configuration
DEBUG = True
'''SECRET_KEY = 'hidden'
USERNAME = 'sayed9sayed@gmail.com'
PASSWORD = '9987861365'

MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=465
MAIL_USE_TLS = False
MAIL_USE_SSL=
MAIL_USERNAME = 'sayed9sayed@gmail.com'
MAIL_PASSWORD = '9987861365'
'''

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = None#'zainul.sayed28@gmail.com'#os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = None#'dgeps6961k'#os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
#app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


#app.config.from_object(__name__)
mail = Mail(app)

print (os.environ.get('MAIL_USERNAME')
       )
@app.route('/')
def send_mail():
    msg = Message(
      'Hello',
       sender='zainul.sayed28@gmail.com ',
       recipients=
       ['sayed9sayed@gmail.com'])
    msg.body = "This is the email body"
    print("sending mail")
    mail.send(msg)
    print ("mail send")
    return "Sent"


if __name__ =="__main__":
    app.run(debug=True)