from flask import render_template, flash, redirect, request, session, url_for, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User
from functools import wraps


chat_blueprint = Blueprint(
    'chat', __name__,
    template_folder='templates'
)

@chat_blueprint.route('/competitors')
def competitors():
    return render_template('competitors.html')
