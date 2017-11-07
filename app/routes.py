from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from app import app, db, lm, admin
from .forms import LoginForm, SignupForm, CompetitionForm
from .models import User, Competition
from datetime import datetime

admin.add_view(ModelView(User, db.session))

@app.route('/')
def index():
  form = LoginForm()
  return render_template('index.html', form=form )

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Disable access to login page if user is already logged in.

    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for('profile'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            email = form.email.data
            password = form.password.data

            session['remember_me'] = form.remember_me.data

            user = User.query.filter_by(email=email).first()

            if user is not None and user.verify_password(password):
                login_user(user)
                flash('Logged in')
                return redirect(url_for('index'))
            else:
                flash('Invalid Login')
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)
  


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # # Disable access to login page if user is already logged in.
    if current_user.is_authenticated:
            flash("You are already signed up!")
            return redirect(url_for('index'))
    form = SignupForm()
    # Checks if form fields are filled
    # if it is, create a new user with provided credentials
    if request.method == 'POST':
        if form.validate_on_submit():
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email

            flash("You have signed up!")
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)
##############
# HOST ROUTE #
##############
@app.route('/host', methods=['GET', 'POST'])
@login_required
def host():
    form = CompetitionForm()

    # form.event.choices =

    if request.method == 'POST':
        if form.validate_on_submit():
            # datetime_object = datetime.strftime(form.date.data, '%Y/%m/%d')
            newcomp = Competition(form.name.data, form.location.data, form.date.data)


            db.session.add(newcomp)
            db.session.commit()

            flash(form.name.data, "has been created!")
            return redirect(url_for('index'))
        else:
            return render_template('host.html', form=form)
    return render_template('host.html', form=form)

@app.route('/manage')
@login_required
def manage():
    competitions = db.session.query(Competition).all()
    return render_template('manage.html', competitions=competitions)


@app.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('event.html', comp=comp)

@app.route('/manage/<comp_id>/announcements')
@login_required
def announcements(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    return render_template('announcements.html', comp=comp)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile-layout.html')

@app.route('/learnmore')
def learnmore():
    return render_template('learnmore.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/eventselected')
def eventselected():
    return render_template('event.html')

#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html'), 404

@app.route('/404')
def error():
    return render_template('404.html')

@app.route('/event-announcements')
def eventAnnouncements():
    events = [('Event 4', 'Announcement 4', 'Today 7:30PM'),('Event 3', 'Announcement 3', 'Today 7:00PM'),
    ('Event 2', 'Announcement 2', 'Today 6:45PM'),('Event 1', 'Announcement 1', 'Today 6:30PM')]
    return render_template('event-announcements.html', eventName="City College Cube Day", list = events)

@app.route('/event-schedule')
def eventSchedule():
    return render_template('event-schedule.html', eventName="City College Cube Day")

def postAnnouncement():
    # Code for posting announcement

    # render template / reload page
    eventAnnouncements()
