from flask import render_template, flash, redirect, request, session, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, SignupForm
from app.models import User
from functools import wraps
from wtforms import ValidationError


users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if current_user.is_authenticated:
            return test(*args, **kwargs)
        else:
            flash('You need to be logged in to access this page!')
            return redirect(url_for('users.login'))
    return wrap



@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # Disable access to login page if user is already logged in.
    if current_user.is_authenticated:
        flash("You are already logged in!")
        return redirect(url_for('profile')) # originally redirected to index

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
                return redirect(url_for('profile'))
            else:
                flash('Invalid Login')
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)



@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))



@users_blueprint.route('/signup', methods=['GET', 'POST']) # we should also make it so that people can't make another account with the same email
def signup():
    # # Disable access to login page if user is already logged in.
    if current_user.is_authenticated:
            flash("You are already signed up!")
            return redirect(url_for('index'))
    form = SignupForm()
    #Check if email was used for another account

    # Checks if form fields are filled
    # if it is, create a new user with provided credentials
    if request.method == 'POST':
        if form.validate_on_submit():
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            if User.query.filter_by(email=form.email.data).first():
                flash("This email is already in use")
                return redirect(url_for('users.signup'))

            db.session.add(newuser)
            db.session.commit()

            flash("You have signed up! Please log in!")
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)