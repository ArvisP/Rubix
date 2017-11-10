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

    return render_template('competition.html', comp=comp)

@manage_blueprint.route('/manage/<comp_id>/announcements')
@login_required
def announcements(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    return render_template('announcements.html', comp=comp)
