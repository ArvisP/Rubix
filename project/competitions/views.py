from flask import render_template, redirect, flash, session, url_for, Blueprint
from flask import request
from flask_login import current_user
from app import app, db
from app.models import Competition, Announcement, Event
from project.users.views import login_required

competitions_blueprint = Blueprint(
    'competitions', __name__,
    template_folder='templates'
)

@competitions_blueprint.route('/competitions')
def competitions():
    competitions = Competition.query.filter_by(approved=True).all()
    return render_template('competitions.html', competitions=competitions)

@competitions_blueprint.route('/competitions/<comp_id>')
def competition(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('comp_info.html', comp=comp)

@competitions_blueprint.route('/competitions/<comp_id>/announcements', methods=['GET', 'POST'])
@login_required
def announcements(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    query = Announcement.query.filter_by(comp_id=comp.comp_id).all()
    announcements = list(reversed(query))

    if request.method == 'POST':
        if form.validate_on_submit():
            newAnnounce = Announcement(comp.comp_id, current_user.wca_id, form.title.data, form.body.data)
            db.session.add(newAnnounce)
            db.session.commit()

            flash('Posted!')
            return redirect(url_for('manage.manage') + "/" + comp_id +"/announcements")
        else:
            flash('Somethings not working')
            return render_template('comp_announcements.html', form=form, comp=comp, announcements=announcements)

    return render_template('comp_announcements.html', comp=comp, announcements=announcements)

@competitions_blueprint.route('/competitions/<comp_id>/schedule')
def schedule(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    return render_template('comp_schedule.html', comp=comp)


@competitions_blueprint.route('/competitions/<comp_id>/schedule/<event_id>', methods=['GET', 'POST'])
def event(comp_id, event_id):

    comp = Competition.query.filter_by(comp_id=comp_id).first()

    event = Event.query.filter_by(event_id=event_id).first()

    return render_template('comp_event.html', comp=comp, event=event)
