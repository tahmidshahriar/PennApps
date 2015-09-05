from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = TextField('password', validators=[Required()])
