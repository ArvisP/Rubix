'''
Routing to general front page things.
'''

from flask import render_template
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, admin
from .models import User, Competition, Event, EventUserLink


#Import project blueprints
from project.users.views import users_blueprint, login_required
from project.host.views import host_blueprint
from project.manage.views import manage_blueprint
from project.competitions.views import competitions_blueprint

class AdminView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Competition, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(EventUserLink, db.session))

app.register_blueprint(users_blueprint)
app.register_blueprint(host_blueprint)
app.register_blueprint(manage_blueprint)
app.register_blueprint(competitions_blueprint)


<<<<<<< HEAD
# Route to the index page
=======


#Route to the index page
>>>>>>> 320452e407447b292fda0f8b655ae9eddd4f0c0a
@app.route('/')
def index():
    '''
    Route to the index page
    '''
    return render_template('index.html')


# Route to the profile page
@app.route('/profile')
@login_required
def profile():
<<<<<<< HEAD
=======

    '''
    Route to the profile page
    '''
    return render_template('profile-layout.html')

#Route to the learn more page

>>>>>>> 320452e407447b292fda0f8b655ae9eddd4f0c0a
    if current_user.credentials == 1:
        return render_template('profile-layout.html')
    elif current_user.credentials == 2:
        return render_template('delegate-layout.html')

<<<<<<< HEAD
=======

>>>>>>> 320452e407447b292fda0f8b655ae9eddd4f0c0a
@app.route('/learnmore')
def learnmore():
    '''
    Route to the learnmore page
    '''
    return render_template('learnmore.html')


# Route to the about page
@app.route('/about')
def about():
    '''
    Route to the about page
    '''
    return render_template('about.html')


@app.route('/announcements')
def announcements():
    return render_template('announcements.html')


@app.route('/comp-competitors')
def competitors():
    return render_template('competitors.html')


@app.route('/comp-schedule')
def schedule():
    return render_template('schedule.html')


# 404 Error handler
@app.route('/404')
def error():
    '''
    Render 404 template
    '''
    return render_template('404.html')
