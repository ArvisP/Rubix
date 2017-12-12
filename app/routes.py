'''
Routing to general front page things.
'''
from flask import render_template, redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, admin
from .models import User, Competition, Event, EventUserLink, ChatHistory
from sqlalchemy import update


#Import project blueprints
from project.users.views import users_blueprint, login_required
from project.host.views import host_blueprint
from project.manage.views import manage_blueprint


class AdminView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Competition, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(EventUserLink, db.session))
admin.add_view(ModelView(ChatHistory, db.session))

app.register_blueprint(users_blueprint)
app.register_blueprint(host_blueprint)
app.register_blueprint(manage_blueprint)

#Route to the index page
@app.route('/')
def index():
    '''
    Route to the index page
    '''
    return render_template('landing_page.html')

@app.route('/competitions')
def competitions():
    competitions = Competition.query.filter_by(approved=True).all()
    return render_template('competitions.html', competitions=competitions)

# Route to the profile page
@app.route('/profile')
@login_required
def profile():
    if current_user.credentials == 1:
        approve_competitions = Competition.query.filter_by(organizer_id=current_user.id).all() #approved=False
        return render_template('user_profile.html', competitions=approve_competitions)

    elif current_user.credentials == 2:
        approve_competitions = Competition.query.filter_by(approved=False, rejected=False).all() # returns all competitions who's approve value is false and reject value is false.
        return render_template('delegate_profile.html', competitions=approve_competitions) #left side is how we access through template, right side is what we wrote inside views function

@app.route('/announcements')
def announcements():
    return render_template('announcements.html')





@app.route('/comp-schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/profile/<comp_id>', methods=['GET','POST'])
@login_required
def accept_competition(comp_id):
    accept_comp = Competition.query.filter_by(comp_id=comp_id).first()
    if request.method =='POST':
        if request.form['decision']=="approve":
            accept_comp.approved = True
               
        elif request.form['decision']=="reject":
            accept_comp.rejected = True

        db.session.add(accept_comp)
        db.session.commit()
    return redirect(url_for('profile'))

# 404 Error handler
@app.route('/404')
def error():
    '''
    Render 404 template
    '''
    return render_template('404.html')
