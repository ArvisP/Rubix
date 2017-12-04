'''
Create forms here
'''
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, SelectMultipleField, DateTimeField
from wtforms_components import TimeField, DateField
from wtforms.validators import DataRequired, Email, Length
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

class LoginForm(FlaskForm):
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
    date = DateField('Date', format="%Y-%m-%d")
    submit = SubmitField('Create competition')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired("Please enter a title")], render_kw={"placeholder": "Title..."})
    body = TextAreaField('Body', validators=[DataRequired("Please enter a body")], render_kw={"placeholder": "Body..."})
    submit = SubmitField('Post announcement')

class ScheduleForm(FlaskForm):
    event = SelectField('Events', choices=[ ('Rubik\'s Cube', 'Rubik\'s Cube'),
                                            ('2x2x2 Cube', '2x2x2 Cube'),
                                            ('4x4x4 Cube', '4x4x4 Cube'),
                                            ('5x5x5 Cube', '5x5x5 Cube'),
                                            ('6x6x6 Cube', '6x6x6 Cube'),
                                            ('7x7x7 Cube', '7x7x7 Cube'),
                                            ('3x3x3 Blindfolded', '3x3x3 Blindfolded'),
                                            ('3x3x3 Fewest Moves', '3x3x3 Fewest Moves'),
                                            ('3x3x3 One Handed', '3x3x3 One Handed'),
                                            ('3x3x3 With Feet', '3x3x3 With Feet'),
                                            ('Megaminx', 'Megaminx'),
                                            ('Pyraminx', 'Pyraminx'),
                                            ('Rubik\'s Clock', 'Rubik\'s Clock'),
                                            ('Skewb', 'Skewb'),
                                            ('Square-1', 'Square-1'),
                                            ('4x4x4 Blindfolded', '4x4x4 Blindfolded'),
                                            ('5x5x5 Blindfolded', '5x5x5 Blindfolded'),
                                            ('3x3x3 Multi-Blind', '3x3x3 Multi-Blind'),
                                            ('Other', 'Other')])
    event_round = SelectField('Round', choices=[ ('Round 1', 'Round 1'),
                                            ('Round 2', 'Round 2'),
                                            ('Final', 'Final'),
                                            ('Combined Final', 'Combined Final')])
    start_time = TimeField('Start time', format='%H:%M')
    end_time = TimeField('End time', format='%H:%M')
    submit = SubmitField('Create competition')

class EventForm(FlaskForm):
    start_time = TimeField('Start time', format='%H:%M')
    end_time = TimeField('End time', format='%H:%M')
    submit = SubmitField('Edit Competition')

class RegisterForm(FlaskForm):
    event = MultiCheckboxField('Events', choices=[ ('Rubik\'s Cube', 'Rubik\'s Cube'),
                                            ('2x2x2 Cube', '2x2x2 Cube'),
                                            ('4x4x4 Cube', '4x4x4 Cube'),
                                            ('5x5x5 Cube', '5x5x5 Cube'),
                                            ('6x6x6 Cube', '6x6x6 Cube'),
                                            ('7x7x7 Cube', '7x7x7 Cube'),
                                            ('3x3x3 Blindfolded', '3x3x3 Blindfolded'),
                                            ('3x3x3 Fewest Moves', '3x3x3 Fewest Moves'),
                                            ('3x3x3 One Handed', '3x3x3 One Handed'),
                                            ('3x3x3 With Feet', '3x3x3 With Feet'),
                                            ('Megaminx', 'Megaminx'),
                                            ('Pyraminx', 'Pyraminx'),
                                            ('Rubik\'s Clock', 'Rubik\'s Clock'),
                                            ('Skewb', 'Skewb'),
                                            ('Square-1', 'Square-1'),
                                            ('4x4x4 Blindfolded', '4x4x4 Blindfolded'),
                                            ('5x5x5 Blindfolded', '5x5x5 Blindfolded'),
                                            ('3x3x3 Multi-Blind', '3x3x3 Multi-Blind'),
                                            ('Other', 'Other')])
    submit = SubmitField('Register')

class VolunteerForm(FlaskForm):
    role = SelectField('Role', choices=[('', '---'),
                                        ('Scrambler', 'Scrambler'),
                                        ('Runner', 'Runner'),
                                        ('Judge', 'Judge')],
                                        default='', validators=[DataRequired('Please select a role')])
    submit = SubmitField('Volunteer')
