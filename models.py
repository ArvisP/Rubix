from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
import urllib2
import json

db = SQLAlchemy()

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120))
  pwdhash = db.Column(db.String(54))

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  class Place(object):
    def query(self, address):
      lat, lng = self.address_to_latlng(address)
      print lat, lng

      query_url = ''
      g = urllib2.urlopen(query_url)
      results = g.read()
      g.close()

      data = json.loads(results)
      print data

      places = []
      for place in data['query']['geusearch']:
        name = place['title']
        meters = place['dist']
        lat = place['lat']
        lng = place['lng']