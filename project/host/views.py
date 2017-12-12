'''
Host routes
'''
from flask import render_template, redirect, flash, url_for, request, Blueprint
from flask_login import current_user
from app import db
from app.models import Competition
from app.forms import CompetitionForm

from project.users.views import login_required

host_blueprint = Blueprint(
    'host', __name__,
    template_folder='templates'
)

@host_blueprint.route('/host', methods=['GET', 'POST'])
@login_required
def host():
    '''
    Manages the host page and all of the data that comes from the form
    '''
    form = CompetitionForm()

    if request.method == 'POST':
        if form.validate_on_submit():

            new_comp = Competition(
                organizer_id=current_user.id,
                title=form.name.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                zipcode=form.zipcode.data,
                date=form.date.data)

            db.session.add(new_comp)
            db.session.commit()

            flash(form.name.data + " has been created!")
            return redirect(url_for('manage.manage'))
        else:
            return render_template('host.html', form=form)
    return render_template('host.html', form=form)
