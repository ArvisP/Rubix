from flask import render_template, redirect, flash, session, url_for, Blueprint
from flask import request
from flask_login import current_user
from app import app, db
from app.models import User, Competition, Announcement, Event, EventUserLink
from project.users.views import login_required
from app.forms import AnnouncementForm, ScheduleForm, EventTimeForm, StaffForm, VolunteerForm, RegisterForm

manage_blueprint = Blueprint(
    'manage', __name__,
    template_folder='templates'
)

@manage_blueprint.route('/manage')
@login_required
def manage():
    # if current_user.credentials == 1:
    #     # print("regular user")
    #     return render_template('404.html')
    # elif current_user.credentials == 2:
    #     # print("current user")
        competitions = Competition.query.filter_by(organizer_id=current_user.id).all()
        return render_template('manage.html', competitions=competitions)

@manage_blueprint.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first() # filters competitions by competition id, returns first competitions
    organizer = User.query.filter_by(id=comp.organizer_id).first()
    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('details.html', comp=comp, organizer=organizer) #left side is how we access through template, right side is what we wrote inside views function

@manage_blueprint.route('/manage/<comp_id>/announcements', methods=['GET', 'POST'])
@login_required
def announcements(comp_id):
    form = AnnouncementForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    query = Announcement.query.filter_by(comp_id=comp.comp_id).all()
    announcements = list(reversed(query))

    if request.method == 'POST':
        if form.validate_on_submit():
            new_announcement = Announcement(comp.comp_id, current_user.id, form.title.data, form.body.data)
            db.session.add(new_announcement)
            db.session.commit()

            flash('Posted!')
            return redirect(url_for('manage.manage') + "/" + comp_id +"/announcements")
        else:
            flash('Somethings not working')
            return render_template('announcements.html', form=form, comp=comp, announcements=announcements)

    return render_template('announcements.html', form=form, comp=comp, announcements=announcements)

@manage_blueprint.route('/manage/<comp_id>/announcements/delete', methods=['POST'])
@login_required
def delete_annc(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    delete_id = Announcement.query.filter_by(annc_id=request.form['post_to_delete']).first()

    db.session.delete(delete_id)
    db.session.commit()
    return redirect(url_for('manage.announcements', comp_id=comp.comp_id))

@manage_blueprint.route('/manage/<comp_id>/newevent', methods=['GET', 'POST'])
@login_required
def newEvent(comp_id):
    form = ScheduleForm()
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            newEvent = Event(form.event.data, form.event_round.data, form.start_time.data, form.end_time.data)
            db.session.add(newEvent)
            comp.comp_events.append(newEvent)
            db.session.commit()

            flash(form.event.data + " event created!")
            return redirect(url_for('manage.event', comp_id=comp.comp_id, event_id=newEvent.event_id))
        else:
            flash('Somethings not working!')
            return render_template('newevent.html', form=form, comp=comp)

    return render_template('newevent.html', form=form, comp=comp)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>', methods=['GET', 'POST'])
@login_required
def event(comp_id, event_id):
    form_vol = VolunteerForm()
    form_reg = RegisterForm()
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    event = Event.query.filter_by(event_id=event_id).first()

    volunteer = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()
    event_volunteers = EventUserLink.query.filter_by(event_id=event_id).filter_by(volunteer=True).all()

    staff = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()
    event_staff = EventUserLink.query.filter_by(event_id=event_id).filter_by(staff=True).all()

    if request.method == 'POST':
        if form.validate_on_submit():
            event.start_time = form.start_time.data
            event.end_time = form.end_time.data

    return render_template('event.html', form_vol=form_vol, form_reg=form_reg, comp=comp, event=event, volunteer=volunteer, event_volunteers=event_volunteers, staff=staff, event_staff=event_staff)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit', methods=['GET', 'POST'])
@login_required
def editEvent(comp_id, event_id):
    form_time = EventTimeForm()
    form_staff = StaffForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    event = Event.query.filter_by(event_id=event_id).first()

    event_users = EventUserLink.query.filter_by(event_id=event_id).all()

    volunteer = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()
    event_volunteers = EventUserLink.query.filter_by(event_id=event_id).all()

    staff = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()
    event_staff = EventUserLink.query.filter_by(event_id=event_id).filter_by(staff=True).all()
    print(event_staff)
    # form.start_time.data = event.start_time
    # form.end_time.data = event.end_time

    if form_time.validate_on_submit():
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        db.session.commit()

        flash(event.event_name + " updated!")
        return redirect(url_for('manage.event', comp_id=comp.comp_id, event_id=event.event_id, volunteer=volunteer, event_volunteers=event_volunteers, staff=staff, event_staff=event_staff))

    return render_template('edit.html', form_staff=form_staff, form_time=form_time, event_users=event_users, comp=comp, event=event, volunteer=volunteer, event_volunteers=event_volunteers, staff=staff, event_staff=event_staff)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/add_volunteer', methods=['POST'])
@login_required
def approveVolunteer(comp_id, event_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    volunteer = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=request.form['volunteer_to_add']).first()

    volunteer.volunteer = True
    db.session.commit()

    return redirect(url_for('manage.editEvent', comp_id=comp_id, event_id=event_id))

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/delete_volunteer', methods=['POST'])
@login_required
def deleteVolunteer(comp_id, event_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    volunteer = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=request.form['volunteer_to_delete']).first()

    volunteer.volunteer = False
    db.session.commit()

    return redirect(url_for('manage.editEvent', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/staff', methods=['GET','POST'])
@login_required
def addStaff(comp_id, event_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    staff = User.query.filter_by(id=request.form['staff_to_add']).first()
    event = Event.query.filter_by(event_id=event_id).first()
    # Check if user is already in event_user_link
    staff_exists = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=staff.id).first()

    if (staff_exists):
        staff_exists.staff = True
    else:
        # Must add the user to event_user_link db first
        register_staff = EventUserLink(user=staff, event=event)
        # Then we append the user to the event and vice versa.
        db.session.add(register_staff)
        # And set their staff to true.
        register_staff.staff = True

    db.session.commit()

    return redirect(url_for('manage.editEvent', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/editstaff', methods=['GET','POST'])
@login_required
def changeStaff(comp_id, event_id):
    form = StaffForm()
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    event = Event.query.filter_by(event_id=event_id).first()
    staff = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=request.form['staff_to_change']).first()

    # And set their staff to true.
    if form.role.data:
        staff.staff_role = form.role.data
    else:
        staff.staff = False

    db.session.commit()

    return redirect(url_for('manage.editEvent', form=form, comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/delete', methods=['POST'])
@login_required
def delete_event(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    delete_link = EventUserLink.query.filter_by(event_id=request.form['event_to_delete']).all()
    delete_id = Event.query.filter_by(event_id=request.form['event_to_delete']).first()

    for link in delete_link:
        db.session.delete(link)

    db.session.delete(delete_id)
    db.session.commit()
    return redirect(url_for('manage.manage_comp', comp_id=comp.comp_id))




@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/register', methods=['GET', 'POST'])
@login_required
def event_register(comp_id, event_id):
    form = RegisterForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    user = User.query.filter_by(id=current_user.id).first()
    event = Event.query.filter_by(event_id=event_id).first()


    if form.validate_on_submit():
        register_user = EventUserLink(user=user, event=event)
        db.session.add(register_user)
        db.session.commit()
        flash('You have registered for this event!')
        return redirect(url_for('manage.event', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/volunteer', methods=['GET', 'POST'])
@login_required
def event_volunteer(comp_id, event_id):
    form = VolunteerForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    user = User.query.filter_by(id=current_user.id).first()
    event = Event.query.filter_by(event_id=event_id).first()
    volunteer = EventUserLink.query.filter_by(event_id=event_id).filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        role = form.role.data

        volunteer.volunteer_role = role
        db.session.commit()

        flash('You have requested to be a volunteer!')
        return redirect(url_for('manage.event', comp_id=comp_id, event_id=event_id))

@manage_blueprint.route('/manage/<comp_id>/register', methods=['GET', 'POST'])
@login_required
def register(comp_id):
    form = RegisterForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    user = User.query.filter_by(id=current_user.id).first()

    comp.competitors.append(user)
    db.session.commit()

    flash('You have been registered to ' + comp.title + "!")
    return redirect(url_for('manage.event', comp_id=comp_id, event_id=event_id))
