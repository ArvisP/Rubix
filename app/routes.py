from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

  # Disable access to login page if user is already logged in.
  # if 'email'in session:
  #   return redirect(url_for('home'))

  form = LoginForm()


  # if request.method == 'POST':
  #   # Checks if form fields are filled
  #   if form.validate_on_submit():
  #     email = form.email.data
  #     password = form.password.data

  #     user = User.query.filter_by(email=email).first()
      
  #     login_user(user)

  #     flash('Logged in')

  #     return redirect(url_for('home'))

  # elif request.method == 'GET':
  return render_template('login.html', form=form)








@app.route('/about')
def about():
  return "hellowordl!"



@app.route('/signup')
def signup():
  return "hellowordl!"