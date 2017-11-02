'''
Create forms here
'''
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
'''
Sign-In / Sign-Up Forms
'''
class SignupForm(Form):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  address = StringField('Address', validators=[DataRequired("Please enter an address.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')

class LoginForm(Form):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  remember_me = BooleanField('remember_me', default=False)
  submit = SubmitField('Sign in')

'''

'''
