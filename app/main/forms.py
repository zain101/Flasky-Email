__author__ = 'zainul'
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import User, Role
from flask.ext.pagedown.fields import PageDownField
class NameForm(Form):
    name = StringField('Email-ID  of your friend?', validators=[Required()])
    message = TextAreaField('Enter your message')
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dollors underscore and peroids')])
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('Aboute me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Email(), Required(), Length(1, 64)])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, numbers, dollors underscore and peroids')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(1, 64)])
    location = StringField('Location', validators=[Length(1, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exist.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exist.')

class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')