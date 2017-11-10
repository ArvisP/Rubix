from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from flask_admin import Admin

admin = Admin(app, name='Rubix', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session))


# IMPORT BLUEPRINTS #
#####################
from project.users.views import users_blueprint
app.register_blueprint(users_blueprint)


from app import routes, models
