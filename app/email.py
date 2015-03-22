__author__ = 'zainul'

from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message

from . import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app= current_app._get_current_object()
    msg= Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+ ' '+subject ,\
                 sender= app.config['FLASKY_MAIL_SENDER'],\
                recipients= ['zainul.sayed28@gmail.com', 'sayed9sayed@gmail.com', 'eyantra2269@gmail.com']\
                )

    msg.body= render_template(template+ '.txt', **kwargs)
    msg.html= render_template(template+ '.html', **kwargs)
    #mail.send(msg)
    thr= Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
