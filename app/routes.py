from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_admin.contrib.sqla import ModelView
from app import app, db, lm, admin
from .forms import LoginForm, SignupForm, CompetitionForm
from .models import User, Competitions
from datetime import datetime

admin.add_view(ModelView(User, db.session))

@app.route('/')
@app.route('/index')
def index():
  number = request.args.get('number')
  return render_template('index.html', number=number)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods=['GET', 'POST'])
def login():

  # Disable access to login page if user is already logged in.
  if current_user.is_authenticated:
    flash("You are already logged in!")
    return redirect(url_for('index'))

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
      newcomp = Competitions(form.name.data, form.location.data, form.date.data)

      db.session.add(newcomp)
      db.session.commit()

      flash(form.name.data, "has been created!")
      return redirect(url_for('index'))
    else:
      return render_template('host.html', form=form)
  return render_template('host.html', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/learnmore')
def learnmore():
  return render_template('learnmore.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/eventselected')
def eventselected():
    return render_template('event.html')
