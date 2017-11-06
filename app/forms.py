'''
Create forms here
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length
'''
Sign-In / Sign-Up Forms
'''
class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  remember_me = BooleanField('remember_me', default=False)
  submit = SubmitField('Sign in')

class CompetitionForm(FlaskForm):
  name = StringField('Competition Name', validators=[DataRequired("Please enter a name for your competition")])
  location = StringField('Location')
  date = DateField('Date', format='%Y-%m-%d')
  event = RadioField('Events', choices=[('rubikscube', 'Rubik\'s Cube'),
                                        ('fourcube', '4x4x4 Cube'),
                                        ('fivecube', '5x5x5 Cube'),
                                        ('sixcube', '6x6x6 Cube'),
                                        ('sevencube', '7x7x7 Cube'),
                                        ('bld', '3x3x3 Blindfolded'),
                                        ('fmc', '3x3x3 Fewest Moves'),
                                        ('oh', '3x3x3 One Handed'),
                                        ('feet', '3x3x3 With Feet'),
                                        ('megaminx', 'Megaminx'),
                                        ('pyraminx', 'Pyraminx'),
                                        ('clock', 'Rubik\'s Clock'),
                                        ('skewb', 'Skewb'),
                                        ('sq1', 'Square-1'),
                                        ('4bld', '4x4x4 Blindfolded'),
                                        ('5bld', '5x5x5 Blindfolded'),
                                        ('mbld', '3x3x3 Multi-Blind'),])


'''

'''
