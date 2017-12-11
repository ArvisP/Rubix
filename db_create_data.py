import datetime
from app import db
from app.models import User, Competition, Announcement, Event

# Add users
db.session.add(User("Test", "Test", "test@test.com", "test123"))
db.session.add(User("firstname", "lastname", "em@il.com", "password"))
session_user = User.query.filter_by(email="test@test.com").first()
session_user2 = User.query.filter_by(email="em@il.com").first()

<<<<<<< HEAD
# Add competitions
db.session.add(Competition(session_user.wca_id, "Rubik's Cube Day", "Cubicle", datetime.date(2017, 12, 31)))
db.session.add(Competition(session_user2.wca_id, "City College Cube Day", "160 Convent Avenue", datetime.date(2017, 12, 31)))
=======
# Add competitionks
db.session.add(Competition(session_user.id, "Rubik's Cube Day", "Cubicle", datetime.date(2017, 12, 31)))
db.session.add(Competition(session_user2.id, "City College Cube Day", "160 Convent Avenue", datetime.date(2017, 12, 31)))
>>>>>>> 64bd84fb15bb4c38cc69375ae2fb7143da21f9b3
session_comp = Competition.query.filter_by(comp_id=1).first()
session_comp2 = Competition.query.filter_by(comp_id=2).first()

session_comp.approved = True

# Add announcement
announce = Announcement(
    session_comp.comp_id,
    session_user.id,
    "4x4 Evemt shorted to combined final",
    "Due to lack of time, we've shortened the 4x4 event to a combined final. We apologize for any inconvenience!"
)

db.session.add(Announcement(1, session_user.id, "Test Announcement", "Test Body"))
db.session.add(announce)

event = Event("Rubik's Cube", "Round 1",datetime.time(11, 0, 0), datetime.time(12, 0, 0))
db.session.add(event)

session_comp.comp_events.append(event)
session_comp.competitors.append(session_user)
session_comp.competitors.append(session_user2)
event.users.append(session_user)
event.users.append(session_user2)

db.session.commit()
