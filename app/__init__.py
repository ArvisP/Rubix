from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from flask_socketio import SocketIO, send, emit

from flask_oauthlib.client import OAuth
from flask_socketio import SocketIO, send


app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
# app.config['SECRET_KEY'] = 'uh23jl13o2j3'
app.config.from_object('config.HerokuDeployConfig')
db = SQLAlchemy(app)
socketio = SocketIO(app)

oauth = OAuth(app)

# Register a connection to the remote application
wca = oauth.remote_app('wca',
                       base_url='https://www.worldcubeassociation.org/api/v0/',
                       request_token_url=None,
                       access_token_url='https://www.worldcubeassociation.org/oauth/token',
                       authorize_url='https://www.worldcubeassociation.org/oauth/authorize',
                       consumer_key='ac5da98d8c8d0ea070939d65cbb0d29a49606d20c8f035719158bd9eee6c6cd6',
                       consumer_secret='f531e05fdc0cf5acf8205c4788e8dc668ef04f0aeca47704897b5f09842759e7',
                       request_token_method='POST',
                       request_token_params={'scope': 'public email dob'}
                       )
# SocketIO junk
socketio = SocketIO(app)

from flask_admin import Admin

admin = Admin(app, name='Rubix', template_mode='bootstrap3')

# IMPORT BLUEPRINTS #
#####################
from project.users.views import users_blueprint
app.register_blueprint(users_blueprint)

lm.login_view = "users.login"

from app import routes, models
