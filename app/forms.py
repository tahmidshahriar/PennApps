from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])

class LunchForm(Form):
	title = TextField('title', validators=[Required()])
	post = TextField('post', validators=[Required()])

class SignupForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
    firstname = TextField('firstname', validators=[Required()])
    lastname = TextField('lastname', validators=[Required()])
    phone = TextField('phone', validators=[Required()])
    email = TextField('email', validators=[Required()])

