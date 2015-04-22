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
    msg= Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+ ' '+subject, \
                 sender= app.config['FLASKY_MAIL_SENDER'],\
                recipients= [to]
                )

    msg.body= render_template(template+ '.txt', **kwargs)
    msg.html= render_template(template+ '.html', **kwargs)
    try:
        with app.open_resource("image.png") as fp:
            msg.attach("image.png", "image/png", fp.read())
    except:
        print "resource not found"
    # mail.send(msg)
    thr= Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
