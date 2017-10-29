'''
This is where to create new database tables
'''

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# import geocoder
# import urllib2
# import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    wca_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    state = db.Column(db.String(30))
    zipcode = db.Column(db.String(10))

    @property
    def password(self):
        return AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, plaintext):
        self.password_hash = generate_password_hash(plaintext)

    def verify_password(self, plaintext):
        return check_password_hash(self.password_hash, plaintext)

    def __repr__(self):
        return '<User {!r}>'.format(self.wca_id)


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