import datetime
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# This association table is used to store the many-to-many relationship between competitions and users
competitions_users = db.Table('competitionsUsers',
                              db.Model.metadata,
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                              db.Column('comp_id', db.Integer, db.ForeignKey('competitions.comp_id')))

# This association table is used to store the many-to-many relationship between competitions and events
competitions_events = db.Table('competitionsEvents',
                               db.Model.metadata,
                               db.Column('comp_id', db.Integer, db.ForeignKey('competitions.comp_id')),
                               db.Column('event_id', db.Integer, db.ForeignKey('events.event_id')))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wca_id = db.Column(db.String(20))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    credentials = db.Column(db.Integer,default=1) #credential type: (1) regular user or (2) WCA delegate
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))
    oauth = db.Column(db.Boolean, default=False)

    competitor_of = db.relationship('Competition', secondary=competitions_users, backref=db.backref('competitor_of'))
    events = db.relationship('Event', secondary='events_users_link')

    # Constructor for new users that use the Sign Up page
    def __init__(self, first_name, last_name, email, password=None, wca_id=None, dob=None):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.email = email.lower()
        self.wca_id = wca_id

        if password is None:
            self.oauth = True
        else:
            self.set_password(password)

        if dob is None:
            self.dob = None
        else:
            self.dob = datetime.strptime(dob, '%Y-%m-%d')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

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
            return unicode(self.id)  # python 2
        except NameError:
            return int(self.id)  # python 3


class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))
    event_round = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    competition = db.relationship('Competition', secondary=competitions_events, backref=db.backref('comp_events'))
    users = db.relationship('User', secondary='events_users_link')

    def __init__(self, event_name, event_round, start_time, end_time):
        self.event_name = event_name
        self.event_round = event_round
        self.start_time = start_time
        self.end_time = end_time


class Competition(db.Model):
    __tablename__ = 'competitions'
    comp_id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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

    def __init__(self, organizer_id, title, address, city, state, zipcode, date):
        self.organizer_id = organizer_id
        self.title = title
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.date = date
        self.approved = False
        self.active = False


class Announcement(db.Model):
    __tablename__ = 'announcements'
    annc_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
        self.time_created = datetime.now()

class EventUserLink(db.Model):
    __tablename__ = 'events_users_link'
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), primary_key=True)
    user_id = db.Column(db.Integer  , db.ForeignKey('users.id'), primary_key=True)
    volunteer = db.Column(db.Boolean, default=False)
    volunteer_role = db.Column(db.String(20))
    staff = db.Column(db.Boolean, default=False)
    staff_role = db.Column(db.String(20))

    user = db.relationship(User, backref=db.backref("user_assoc"))
    event = db.relationship(Event, backref=db.backref("event_assoc"))
