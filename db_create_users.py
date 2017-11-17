import datetime
from app import db
from app.models import User, Competition, Announcement

# Add users
db.session.add(User("Test", "Test", "test@test.com", "test123"))
db.session.add(User("firstname", "lastname", "em@il.com", "password"))
session_user = User.query.filter_by(email="test@test.com").first()

# Add competitionks
db.session.add(Competition(session_user.wca_id, "Rubik's Cube Day", "Cubicle", datetime.date(2017, 12, 31)))
session_comp = Competition.query.filter_by(comp_id=1).first()

# Add announcement
announce = Announcement(
    session_comp.comp_id,
    session_user.wca_id,
    "4x4 Evemt shorted to combined final",
    "Due to lack of time, we've shortened the 4x4 event to a combined final. We apologize for any inconvenience!"
)

db.session.add(Announcement(1, session_user.wca_id, "Test Announcement", "Test Body"))
db.session.add(announce)

db.session.commit()
