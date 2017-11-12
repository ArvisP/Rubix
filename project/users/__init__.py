from app import app
from app.models import User
from flask_login import LoginManager
lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
