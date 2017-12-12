'''
Routing for user views, login and signup
'''
from functools import wraps

from flask import render_template, flash, redirect, request, session, url_for, Blueprint
from flask_login import login_user, logout_user, current_user
from app import db, wca
from app.forms import LoginForm, SignupForm
from app.models import User
from wtforms import ValidationError


users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)


def login_required(test):
    '''
    Custom login required decorator
    '''
    @wraps(test)
    def wrap(*args, **kwargs):
        '''
        Wrapper
        '''
        if current_user.is_authenticated:
            return test(*args, **kwargs)
        else:
            flash('You need to be logged in to access this page!')
            return redirect(url_for('users.login'))
    return wrap


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Allows user to login
    '''
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

            # checks to see if user is WCA member, if they are do this
            if user is not None and user.oauth is True:
                flash('You are registered using your WCA ID. Please login using your WCA ID.')
                return redirect(url_for('users.login'))

            elif user is not None and user.verify_password(password): #if they are not do this
                login_user(user)
                flash('Logged in')
                return redirect(url_for('profile'))

            else:
                flash('Invalid Login')
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@users_blueprint.route('/wca_login')
def wca_login():
    '''
    logic for WCA Login
    '''
    return wca.authorize(callback=url_for('users.authorized', _external=True))


@users_blueprint.route('/logout')
@login_required
def logout():
    '''
    Logout functionality
    '''
    if get_wca_oauth_token() is not None:
        del session['wca_token']

    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('index'))


@users_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Allow visitor to signup
    '''
    # # Disable access to login page if user is already logged in.
    if current_user.is_authenticated:
        flash("You are already signed up!")
        return redirect(url_for('index'))
    form = SignupForm() # created an instance of SignupForm() and called it "form"
    # Check if email was used for another account

    # Checks if form fields are filled
    # if it is, create a new user with provided credentials
    if request.method == 'POST':
        if form.validate_on_submit():

            if User.query.filter_by(email=form.email.data).first():
                flash("This email is already in use")
                return redirect(url_for('users.signup'))

            new_user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                wca_id=None,
                dob=None
                )
            new_user.credentials = 1

            db.session.add(new_user)
            db.session.commit()

            flash("You have successfully signed up! Please log in!")
            return redirect(url_for('index'))
        else:
            return render_template('signup.html', form=form)

    return render_template('signup.html', form=form)


@users_blueprint.route('/authorized')
def authorized():
    """
    This method fetches all relevant information from the
    WCA remote application and process it accordingly.

    If the remote app sends a blank response or blank access token,
    return an error message to the client

    Otherwise, store the token to the client's session dict
    and check whether the WCA ID of the authenticated user
    exist in the database. If the WCA ID is not found, a new account
    is created for them.

    In either case, the authenticated user will be logged in

    :return: appropriate redirection according to whether the user
    has been successfully authenticated or not.
    """
    resp = wca.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['wca_token'] = (resp['access_token'], '')
    me = wca.get('me').data['me']

    user = User.query.filter_by(wca_id=me['wca_id']).first()

    if user is not None:
        login_user(user)
        flash('Logged in')
        return redirect(url_for('profile'))
    else:
        new_user_data = extract_info(me)
        new_user = User(
            first_name=new_user_data['first_name'],
            last_name=new_user_data['last_name'],
            email=new_user_data['email'],
            password=None,
            wca_id=new_user_data['wca_id'],
            dob=new_user_data['dob']
        )

        if new_user_data['is_delegate']:
            new_user.credentials = 2
        else:
            new_user.credentials = 1

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('You have been signed up and logged in!')
        return redirect(url_for('profile'))


@wca.tokengetter
def get_wca_oauth_token():
    """
    This method is required by OAuth Client implementation
    to work correctly. This method and its associated decorator
    is used by OAuth Client to get to the access token
    :return: a string containing the WCA Token
    """
    return session.get('wca_token')


def extract_info(me):
    """
    This method extracts information returned by the response from WCA OAuth
    :param me: a dictionary containing user information from WCA
    :return: a tuple that contains pertinent information about the user that
    can be used to either login or signup the user
    """
    name = me['name'].split(' ')
    first_name = name[0]
    last_name = name[1]

    wca_id = me['wca_id']
    dob = me['dob']
    email = me['email']

    if me['delegate_status'] is None:
        is_delegate = False
    else:
        is_delegate = True

    return {'wca_id': wca_id, 'first_name': first_name, 'last_name': last_name,
            'dob': dob, 'email': email, 'is_delegate': is_delegate}

