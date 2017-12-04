import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

competitions_users = db.Table('competitionsUsers',
                        db.Model.metadata,
                        db.Column('wca_id', db.Integer, db.ForeignKey('users.wca_id')),
                        db.Column('comp_id', db.Integer, db.ForeignKey('competitions.comp_id')))

# This association table is used to store the many-to-many relationship between competitions and events
competitions_events = db.Table('competitionsEvents',
                               db.Model.metadata,
                               db.Column('comp_id', db.Integer, db.ForeignKey('competitions.comp_id')),
                               db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')))

events_users = db.Table('eventsUsers',
                db.Model.metadata,
                db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')),
                db.Column('wca_id', db.Integer, db.ForeignKey('users.wca_id')))

events_volunteers = db.Table('eventsVolunteers',
                    db.Model.metadata,
                    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')),
                    db.Column('vol_id', db.Integer, db.ForeignKey('volunteers.vol_id')))


events_staff = db.Table('eventsStaff',
                    db.Model.metadata,
                    db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')),
                    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staff_id')))

users_volunteers = db.Table('usersVolunteers',
                    db.Model.metadata,
                    db.Column('wca_id', db.Integer, db.ForeignKey('users.wca_id')),
                    db.Column('vol_id', db.Integer, db.ForeignKey('volunteers.vol_id')))


users_staff = db.Table('usersStaff',
                    db.Model.metadata,
                    db.Column('wca_id', db.Integer, db.ForeignKey('users.wca_id')),
                    db.Column('staff_id', db.Integer, db.ForeignKey('staff.staff_id')))

class User(db.Model):
    __tablename__ = 'users'
    wca_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    credentials = db.Column(db.Integer,default=1) #credential type: (1) regular user or (2) WCA delegate
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))

    competitor_of = db.relationship('Competition', secondary=competitions_users, backref=db.backref('competitor_of'))
    in_event = db.relationship('Event', secondary=events_users, backref=db.backref('in_event'))
    volunteers_in = db.relationship('Volunteer', secondary=users_volunteers, backref=db.backref('volunteers_in'))
    staff_in = db.relationship('Staff', secondary=users_staff, backref=db.backref('staff_in'))

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

    # def __repr__(self):
    #     return '<User {!r}>'.format(self.wca_id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.wca_id)  # python 2
        except NameError:
            return str(self.wca_id)  # python 3




class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))
    event_round = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    competition = db.relationship('Competition', secondary=competitions_events, backref=db.backref('comp_events'))
    competitors = db.relationship('User', secondary=events_users, backref=db.backref('events_users'))
    volunteers = db.relationship('Volunteer', secondary=events_volunteers, backref=db.backref('events_volunteers'))
    staff = db.relationship('Staff', secondary=events_staff, backref=db.backref('events_staff'))

    def __init__(self, event_name, event_round, start_time, end_time):
        self.event_name = event_name
        self.event_round = event_round
        self.start_time = start_time
        self.end_time = end_time


class Competition(db.Model):
    __tablename__ = 'competitions'
    comp_id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.wca_id'))
    title = db.Column(db.String(50))
    date = db.Column(db.Date)
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))

    approved = db.Column(db.Boolean)
    active = db.Column(db.Boolean)

    organizerRel = db.relationship('User', backref='competitionRel')
    events = db.relationship('Event', secondary=competitions_events, order_by="Event.start_time")
    competitors = db.relationship('User', secondary=competitions_users)


    def __init__(self, organizer_id, title, address, date):
        self.organizer_id = organizer_id
        self.title = title
        self.address = address
        self.date = date
        self.approved = False
        self.active = False

class Announcement(db.Model):
    __tablename__ = 'announcements'
    annc_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.wca_id'))
    time_created = db.Column(db.DateTime)
    title = db.Column(db.String(50))
    body = db.Column(db.Text)

    authorRel = db.relationship('User', backref='announcementRel')
    competitionRel = db.relationship('Competition', backref='announcementRel')

    def __init__(self, comp_id, author_id, title, body):
        self.comp_id = comp_id
        self.author_id = author_id
        self.title = title
        self.body = body
        self.time_created = datetime.datetime.now()

class Volunteer(db.Model):
    __tablename__ = 'volunteers'
    vol_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    role = db.Column(db.String(20))
    approved = db.Column(db.Boolean)

    event = db.relationship('Event', secondary=events_volunteers, backref=db.backref('events_volunteers'))
    user = db.relationship('User', secondary=users_volunteers, backref=db.backref('users_volunteers'))

    def __init__(self, user_id, event_id, role):
        self.user_id = user_id
        self.event_id = event_id
        self.role = role
        self.approved = False

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))

    event = db.relationship('Event', secondary=events_staff, backref=db.backref('events_staff'))
    user = db.relationship('User', secondary=users_staff, backref=db.backref('users_staff'))

    def __init__(self, user_id, event_id):
        self.user_id = user_id
        self.event_id = event_id


