from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
app.config.from_object('config.BaseConfig')
db = SQLAlchemy(app)

from flask_admin import Admin

admin = Admin(app, name='Rubix', template_mode='bootstrap3')


# IMPORT BLUEPRINTS #
#####################
from project.users.views import users_blueprint
app.register_blueprint(users_blueprint)


lm.login_view = "users.login"

from app import routes, models
