'''__author__ = 'zainul'
import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for, flash
from flask.ext.script import Manager, Shell
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#  .........................................................Config for database

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# ............................................................config for email
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']=  465
app.config['MAIL_USE_TLS']= False

app.config['MAIL_USE_SSL']= True
app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']= os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_ADMIN'] = 'zainul.sayed28@gmail.com'
app.config['FLASKY_MAIL_SENDER'] = 'zainul.sayed28@gmail.com'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail=Mail(app)
migrate= Migrate(app, db)

manager.add_command('db', MigrateCommand)
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
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

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username= form.name.data).first()
        if user is  None:
            user= User(username= form.name.data)
            db.session.add(user)
            db.session.commit()
            session['know']= False
            flash('First time user')
            send_email(app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
        else:
            session['known']= True
            flash('Registered user ')
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data= ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),  current_time= datetime.utcnow(), known= session.get('known', False))


if __name__ == '__main__':
    #db.create_all()
    manager.run()

'''