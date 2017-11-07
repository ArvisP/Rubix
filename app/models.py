from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))

    def __init__(self, first_name, last_name, email, password):
      self.first_name = first_name.title()
      self.last_name = last_name.title()
      self.email = email.lower()
      self.set_password(password)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)
    # @property
    # def password(self):
    #     return AttributeError('Password is not a readable attribute')

    # @password.setter
    # def password(self, plaintext):
    #     self.password_hash = generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

    def __repr__(self):
        return '<User {!r}>'.format(self.wca_id)

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


class Competition(db.Model):
    __tablename__ = 'competitions'
    comp_id = db.Column(db.Integer, primary_key=True)
    wca_id = db.Column(db.Integer, db.ForeignKey('users.wca_id'))
    title = db.Column(db.String(50))
    date = db.Column(db.Date)
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))

    organizerRel = db.relationship('User', backref='competitionRel')

    def __repr__(self):
        return 'Event {!r} with id {!d}'.format(self.title, self.comp_id)


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

    def __repr__(self):
        return 'This announcement has the id {!d} with title {!s}'.format(self.annc_id, self.title)


class Event(db.Model):
    __tablename__ = "events"
    event_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    event_name = db.Column(db.String(50))

    competitionRel = db.relationship('Competition', backref='eventRel')

    def __repr__(self):
        return "The event id is {!d} and competition id is {!d}".format(self.event_id, self.comp_id)


class Schedule(db.Model):
    __tablename__ = "schedules"
    schedule_id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competitions.comp_id'))
    event_id = db.Column(db.Integer)
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    event_name = db.Column(db.String(50))

    competitionRel = db.relationship('Competition', backref='scheduleRel')

    def __repr__(self):
        return "The scheduled event has the id {!d} for the competition {!d}".format(self.schedule_id, self.comp_id)


class CompetitorRecord(db.Model):
    __tablename__ = "competitorRecords"
    wca_id = db.Column(db.Integer)
    comp_id = db.Column(db.Integer)
    event_id = db.Column(db.Integer)
    # TODO: Additional fields might be added here for the purpose of keeping
    # the result of the event competition for each participant

    def __repr__(self):
        return "The competitor record has the WCA ID of {!d}, Comp ID of {!d} and Event ID of {!d}".format(self.wca_id,
                                                                                                           self.comp_id,
                                                                                                           self.event_id)