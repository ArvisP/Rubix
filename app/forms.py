'''
Create forms here
'''
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields.html5 import DateField
'''
Sign-In / Sign-Up Forms
'''
class SignupForm(FlaskForm):
  first_name = StringField('First name', validators=[DataRequired("Please enter your first name.")])
  last_name = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
  email = StringField('Email', validators=[DataRequired("Please enter your email."), Email("Please enter a valid email.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password."), Length(min=6, message="Passwords must be 6 characters or more.")])
  confirm = PasswordField('Repeat Password')
  submit = SubmitField('Sign up')

<<<<<<< HEAD
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True
'''
class LoginForm(FlaskForm):
=======
class LoginForm(Form):
>>>>>>> 2f8b2a839a01861d12c33e665c77369518b3a345
  email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
  remember_me = BooleanField('remember_me', default=False)
  submit = SubmitField('Sign in')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CompetitionForm(FlaskForm):
  name = StringField('Competition Name', validators=[DataRequired("Please enter a name for your competition")])
  location = TextAreaField('Location')
  date = DateField('Date')
  events = MultiCheckboxField('Events', choices=[('rubikscube', 'Rubik\'s Cube'),
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
                                        ('bld4', '4x4x4 Blindfolded'),
                                        ('bld5', '5x5x5 Blindfolded'),
                                        ('mbld', '3x3x3 Multi-Blind')])
  submit = SubmitField('Create competition')


'''

'''
