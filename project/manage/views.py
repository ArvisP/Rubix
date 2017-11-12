from flask import render_template, redirect, flash, session, url_for, Blueprint
from app import app, db
from app.models import Competition
from project.users.views import login_required

manage_blueprint = Blueprint(
    'manage', __name__,
    template_folder='templates'
)

@manage_blueprint.route('/manage')
@login_required
def manage():
    competitions = db.session.query(Competition).all()
    return render_template('manage.html', competitions=competitions)


@manage_blueprint.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('announcements.html', comp=comp)

@manage_blueprint.route('/manage/<comp_id>/announcements')
@login_required
def announcements(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    events = [('Event 4', 'Announcement 4', 'Today 7:30PM'),('Event 3', 'Announcement 3', 'Today 7:00PM'),
    ('Event 2', 'Announcement 2', 'Today 6:45PM'),('Event 1', 'Announcement 1', 'Today 6:30PM')]

    return render_template('announcements.html', comp=comp, eventName="City College Cube Day", list = events)

@app.route('/manage/<comp_id>/schedule')
def eventSchedule(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    return render_template('schedule.html', comp = comp, eventName="City College Cube Day")
