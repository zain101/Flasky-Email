from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from datetime import datetime
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username = form.name.data).first()
        if user is  None:
            user= User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['know']= False
            #flash('First time user')
            send_email(current_app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known']= True
            pass
            #flash('Registered user ')
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            pass
            #flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data= ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'),  current_time=datetime.utcnow(), known=session.get('known', False))
