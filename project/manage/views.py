'''Routing for managing and viewing a competition.'''


from flask import render_template, redirect, flash, url_for, Blueprint
from flask import request
from flask_login import current_user
from app import app, db, socketio

from app.models import Competition, Announcement, Event, ChatHistory

from app.models import User, Competition, Announcement, Event, EventUserLink

from project.users.views import login_required
from app.forms import AnnouncementForm,\
                        ScheduleForm,\
                        EventTimeForm,\
                        StaffForm,\
                        VolunteerForm,\
                        RegisterForm

manage_blueprint = Blueprint(
    'manage', __name__,
    template_folder='templates'
)

@manage_blueprint.route('/manage')
@login_required
def manage():
    '''
    Displays competitions that are owned by the current logged in user.
    '''
    competitions = Competition.query.filter_by(organizer_id=current_user.id).all()
    return render_template('manage.html', competitions=competitions)

@manage_blueprint.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    '''
    Routes to the competition indicated by <comp_id> and displays the details page by default
    '''
    # filters competitions by competition id, returns first competitions
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    organizer = User.query.filter_by(id=comp.organizer_id).first()
    if comp is None:
        flash('Competition is not found.')
        return redirect(url_for('index'))
    #left side is how we access through template, right side is what we wrote inside views function
    return render_template('details.html', comp=comp, organizer=organizer)

@manage_blueprint.route('/manage/<comp_id>/announcements', methods=['GET', 'POST'])
@login_required
def announcements(comp_id):
    '''
    Routing to the competition's announcements page.
    '''
    form = AnnouncementForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    query = Announcement.query.filter_by(comp_id=comp.comp_id).all()
    announce_list = list(reversed(query))

    if request.method == 'POST':
        if form.validate_on_submit():
            new_announcement = Announcement(comp.comp_id,\
                                            current_user.id,\
                                            form.title.data,\
                                            form.body.data)
            db.session.add(new_announcement)
            db.session.commit()

            flash('Posted!')
            return redirect(url_for('manage.manage') + "/" + comp_id +"/announcements")
        else:
            flash('Somethings not working')
            return render_template('announcements.html',\
                                    form=form,\
                                    comp=comp,\
                                    announce_list=announce_list)

    return render_template('announcements.html', form=form, comp=comp, announce_list=announce_list)

@manage_blueprint.route('/manage/<comp_id>/announcements/delete', methods=['POST'])
@login_required
def delete_annc(comp_id):
    '''
    Deletes the announcement through the annc_id taken provided by the delete button
    '''

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    delete_id = Announcement.query.filter_by(annc_id=request.form['post_to_delete']).first()

    db.session.delete(delete_id)
    db.session.commit()
    return redirect(url_for('manage.announcements', comp_id=comp.comp_id))

@manage_blueprint.route('/manage/<comp_id>/newevent', methods=['GET', 'POST'])
@login_required
def create_event(comp_id):
    '''
    Creates a new event in the competition
    '''
    form = ScheduleForm()
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_event = Event(form.event.data,\
                            form.event_round.data,\
                            form.start_time.data,\
                            form.end_time.data)
            db.session.add(new_event)
            comp.comp_events.append(new_event)
            db.session.commit()

            flash(form.event.data + " event created!")
            return redirect(url_for('manage.event',\
                                    comp_id=comp.comp_id,\
                                    event_id=new_event.event_id))
        else:
            flash('Somethings not working!')
            return render_template('newevent.html', form=form, comp=comp)

    return render_template('newevent.html', form=form, comp=comp)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>', methods=['GET', 'POST'])
@login_required
def event(comp_id, event_id):
    '''
    Displays the selected event and its competitors, volunteers, and staff
    '''
    form_vol = VolunteerForm()
    form_reg = RegisterForm()
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    current_event = Event.query.filter_by(event_id=event_id).first()

    volunteer = EventUserLink.query.filter_by(event_id=event_id).\
                                    filter_by(user_id=current_user.id).first()
    event_volunteers = EventUserLink.query.filter_by(event_id=event_id).\
                                            filter_by(volunteer=True).all()

    staff = EventUserLink.query.filter_by(event_id=event_id).\
                                filter_by(user_id=current_user.id).first()

    event_staff = EventUserLink.query.filter_by(event_id=event_id).\
                                        filter_by(staff=True).all()

    return render_template('event.html',\
                            form_vol=form_vol,\
                            form_reg=form_reg,\
                            comp=comp,\
                            current_event=current_event,\
                            volunteer=volunteer,\
                            event_volunteers=event_volunteers,\
                            staff=staff,\
                            event_staff=event_staff)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(comp_id, event_id):
    '''
    Edit event page, allows volunteer-staff-competitor and time editing
    '''
    form_time = EventTimeForm()
    form_staff = StaffForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    current_event = Event.query.filter_by(event_id=event_id).first()

    event_users = EventUserLink.query.filter_by(event_id=event_id).all()

    volunteer = EventUserLink.query.filter_by(event_id=event_id).\
                                    filter_by(user_id=current_user.id).first()

    event_volunteers = EventUserLink.query.filter_by(event_id=event_id).all()

    staff = EventUserLink.query.filter_by(event_id=event_id).\
                                        filter_by(user_id=current_user.id).first()

    event_staff = EventUserLink.query.filter_by(event_id=event_id).\
                                                filter_by(staff=True).all()

    if form_time.validate_on_submit():
        current_event.start_time = form_time.start_time.data
        current_event.end_time = form_time.end_time.data
        db.session.commit()

        flash(current_event.event_name + " updated!")
        return redirect(url_for('manage.event',\
                                comp_id=comp.comp_id,\
                                event_id=event.event_id,\
                                volunteer=volunteer,\
                                event_volunteers=event_volunteers,\
                                staff=staff,\
                                event_staff=event_staff))

    return render_template('edit.html',\
                            form_staff=form_staff,\
                            form_time=form_time,\
                            event_users=event_users,\
                            comp=comp,\
                            current_event=current_event,\
                            volunteer=volunteer,\
                            event_volunteers=event_volunteers,\
                            staff=staff,\
                            event_staff=event_staff)

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/add_volunteer',\
                        methods=['POST'])
@login_required
def approve_volunteer(comp_id, event_id):
    '''
    Approves the selected volunteer provided by button value
    '''
    volunteer = EventUserLink.query.filter_by(event_id=event_id).\
                                    filter_by(user_id=request.form['volunteer_to_add']).first()

    volunteer.volunteer = True
    db.session.commit()

    return redirect(url_for('manage.edit_event', comp_id=comp_id, event_id=event_id))

@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/delete_volunteer',\
                        methods=['POST'])
@login_required
def delete_volunteer(comp_id, event_id):
    '''
    Deletes the selected volunteer provided by button value
    '''
    volunteer = EventUserLink.query.filter_by(event_id=event_id).\
                                    filter_by(user_id=request.form['volunteer_to_delete']).first()

    volunteer.volunteer = False
    db.session.commit()

    return redirect(url_for('manage.edit_event', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/staff', methods=['GET', 'POST'])
@login_required
def add_staff(comp_id, event_id):
    '''
    Adds the selected staff provided by button value
    '''
    staff = User.query.filter_by(id=request.form['staff_to_add']).first()
    current_event = Event.query.filter_by(event_id=event_id).first()
    # Check if user is already in event_user_link
    staff_exists = EventUserLink.query.filter_by(event_id=event_id).\
                                        filter_by(user_id=staff.id).first()

    if staff_exists:
        staff_exists.staff = True
    else:
        # Must add the user to event_user_link db first
        register_staff = EventUserLink(user=staff, event=current_event)
        # Then we append the user to the event and vice versa.
        db.session.add(register_staff)
        # And set their staff to true.
        register_staff.staff = True

    db.session.commit()

    return redirect(url_for('manage.edit_event', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/edit/editstaff',\
                        methods=['GET', 'POST'])
@login_required
def change_staff(comp_id, event_id):
    '''
    Changes the role of the staff. If the role of the staff is blank, removes from
    staff list
    '''
    form = StaffForm()
    staff = EventUserLink.query.filter_by(event_id=event_id).\
                                filter_by(user_id=request.form['staff_to_change']).first()

    # And set their staff to true.
    if form.role.data:
        staff.staff_role = form.role.data
    else:
        staff.staff = False

    db.session.commit()

    return redirect(url_for('manage.edit_event', form=form, comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/delete', methods=['POST'])
@login_required
def delete_event(comp_id):
    '''
    Deletes selected event and all event_user_links associated with the event
    '''
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
    '''
    Allows the current user to register into selected event
    '''
    form = RegisterForm()

    user = User.query.filter_by(id=current_user.id).first()
    current_event = Event.query.filter_by(event_id=event_id).first()


    if form.validate_on_submit():
        register_user = EventUserLink(user=user, event=current_event)
        db.session.add(register_user)
        db.session.commit()
        flash('You have registered for this event!')
        return redirect(url_for('manage.event', comp_id=comp_id, event_id=event_id))


@manage_blueprint.route('/manage/<comp_id>/schedule/<event_id>/volunteer', methods=['GET', 'POST'])
@login_required
def event_volunteer(comp_id, event_id):
    '''
    Current user can request to volunteer for an event
    '''
    form = VolunteerForm()

    volunteer = EventUserLink.query.filter_by(event_id=event_id).\
                                    filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        role = form.role.data

        volunteer.volunteer_role = role
        db.session.commit()

        flash('You have requested to be a volunteer!')
        return redirect(url_for('manage.event', comp_id=comp_id, event_id=event_id))

@manage_blueprint.route('/manage/<comp_id>/register', methods=['GET', 'POST'])
@login_required
def register(comp_id):
    '''
    Current user can register to a competition
    '''

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    user = User.query.filter_by(id=current_user.id).first()

    comp.competitors.append(user)
    db.session.commit()

    flash('You have been registered to ' + comp.title + "!")
    return redirect(url_for('manage.manage_comp', comp_id=comp_id))

@manage_blueprint.route('/manage/<comp_id>/chat', methods=['GET', 'POST'])
@login_required
def chat(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    return render_template('chat_view.html', comp=comp, comp_id=comp_id)

@socketio.on('load')
def competitors(comp_id): #comp_id
    msgs = ChatHistory.query.filter_by(comp_id=comp_id).all()
    items = []
    for item in msgs:
        items+=[(item.sender, item.message)]
    socketio.emit( 'chat_history', items )


@socketio.on( 'message' )
def handleMessage(comp_id, msg):
    name = current_user.first_name + " " +current_user.last_name
    count = ChatHistory.query.count()+1
    toAdd = ChatHistory(table_id=count, comp_id=comp_id, sender=name, message=msg)
    db.session.add(toAdd)
    db.session.commit()
    socketio.emit( 'my_response', [name, msg] )

