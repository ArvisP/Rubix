from flask import render_template, flash, redirect, request, session, url_for
from flask_admin.contrib.sqla import ModelView
from app import app, db, admin
from .forms import CompetitionForm
from .models import User, Competition
from datetime import datetime

admin.add_view(ModelView(User, db.session))

from functools import wraps

from project.users.views import users_blueprint, login_required

app.register_blueprint(users_blueprint)

@app.route('/')
def index():
    return render_template('index.html')

##############
# HOST ROUTE #
##############
@app.route('/host', methods=['GET', 'POST'])
@login_required
def host():
    form = CompetitionForm()

    # form.event.choices =

    if request.method == 'POST':
        if form.validate_on_submit():
            # datetime_object = datetime.strftime(form.date.data, '%Y/%m/%d')
            newcomp = Competition(form.name.data, form.location.data, form.date.data)


            db.session.add(newcomp)
            db.session.commit()

            flash(form.name.data, "has been created!")
            return redirect(url_for('index'))
        else:
            return render_template('host.html', form=form)
    return render_template('host.html', form=form)

@app.route('/manage')
@login_required
def manage():
    competitions = db.session.query(Competition).all()
    return render_template('manage.html', competitions=competitions)


@app.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('competition.html', comp=comp)

@app.route('/manage/<comp_id>/announcements')
@login_required
def announcements(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    return render_template('announcements.html', comp=comp)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile-layout.html')

@app.route('/learnmore')
def learnmore():
    return render_template('learnmore.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/eventselected')
def eventselected():
    return render_template('event.html')

#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html'), 404

@app.route('/404')
def error():
    return render_template('404.html')

@app.route('/event-announcements')
def eventAnnouncements():
    events = [('Event 4', 'Announcement 4', 'Today 7:30PM'),('Event 3', 'Announcement 3', 'Today 7:00PM'),
    ('Event 2', 'Announcement 2', 'Today 6:45PM'),('Event 1', 'Announcement 1', 'Today 6:30PM')]
    return render_template('event-announcements.html', eventName="City College Cube Day", list = events)

@app.route('/event-schedule')
def eventSchedule():
    return render_template('event-schedule.html', eventName="City College Cube Day")

def postAnnouncement():
    # Code for posting announcement

    # render template / reload page
    eventAnnouncements()
