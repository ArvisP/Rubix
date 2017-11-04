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


class Competitions(db.Model):
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