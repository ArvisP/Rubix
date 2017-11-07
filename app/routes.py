from flask import render_template, flash, redirect, request, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, SignupForm
from .models import User

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
  if 'email' in session:
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
  return render_template('index.html', form=form)


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  # # Disable access to login page if user is already logged in.
  if 'email' in session:
    flash("You are already logged in!")
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
      return redirect(url_for('index'))
    else:
      return render_template('signup.html', form=form)

  return render_template('signup.html', form=form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/profile')
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
#@app.route('/404')
#def error():
#  return render_template('404.html')

# @app.route('/signup')
# def signup():
#   return "hellowordl!"
