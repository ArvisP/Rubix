from app import app
from flask_login import LoginManager
lm = LoginManager()
lm.init_app(app)
