from app import app, db
from flask import request
from werkzeug.security import check_password_hash

import unittest
import datetime

from flask_testing import TestCase
from flask_login import current_user
from app.models import User, Competition, Announcement, Event, EventUserLink

class BaseTestCase(TestCase):
    '''
    Initializes he app
    '''
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app
    '''
    Creates the database and adds data to the database
    '''
    def setUp(self):
        db.create_all()
        db.session.add(User("Firstname", "Lastname", "test@test.com", "test123"))
        db.session.add(User("Mock", "User", "mock@user.com", "mock123"))
        db.session.add(User("new", "User", "new@user.com", "new123"))
        db.session.add(User("Competitor", "Jones", "comp@jones.com", "comp123"))
        user = User.query.filter_by(email="test@test.com").first()
        user1 = User.query.filter_by(email="new@user.com").first()
        user2 = User.query.filter_by(email="comp@jones.com").first()

        db.session.add(Competition(user.id, "Test name", "Test location", "Test City", "Test State", "10031", datetime.date(2017, 12, 31)))
        db.session.add(Competition(20, "Cant view", "Cant view", "New York", "NY", "10031", datetime.date(2017, 12, 31)))
        comp = Competition.query.filter_by(comp_id=1).first()
        comp.approved = True
        comp20 = Competition.query.filter_by(organizer_id=20).first()

        announce1 = Announcement(comp.comp_id, user.id, "Test announcement", "Test body")
        announce2 = Announcement(comp20.comp_id, 2, "Can i see this?", "maybe")
        db.session.add(announce1)
        db.session.add(announce2)

        event1 = Event('4x4x4 Cube', 'Round 1', datetime.time(11, 0, 0), datetime.time(12, 0, 0))
        db.session.add(event1)
        comp.comp_events.append(event1)
        comp.competitors.append(user)
        comp.competitors.append(user1)
        comp.competitors.append(user2)

        register_user1 = EventUserLink(user=user1, event=event1)
        register_user2 = EventUserLink(user=user2, event=event1)
        db.session.add(register_user1)
        db.session.add(register_user2)
        register_user2.volunteer = True
        register_user2.volunteer_role = 'Judge'
        register_user1.staff = True
        register_user1.staff_role = 'Scrambler'

        db.session.commit()

    '''
    Drops all tables from the database
    '''
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

class TestBasic(BaseTestCase):
    '''Ensure that flask was set up correctly'''
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class TestUser(BaseTestCase):
    def test_user_signup(self):
        with self.client:
            response = self.client.post(
                '/signup',
                data=dict(
                    first_name="New", last_name="User",
                    email="new@user.com", password="newuser"
                ),
                follow_redirects=True
            )
            user = User.query.filter_by(email="new@user.com").first()
            self.assertTrue(user)

    def test_incorrect_user_signup(self):
        with self.client:
            response = self.client.post(
                '/signup',
                data=dict(
                    first_name="New", last_name="User",
                    email="newuser", password="newuser"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Please enter a valid email.', response.data)
            self.assertIn('/signup', request.url)

    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertIn(b'Log in', response.data)

    def test_login(self):
        with self.client:
            response = self.login('test@test.com', 'test123')
            # self.assertIn(b'Logged in', response.data)
            self.assertTrue(current_user.email == "test@test.com")

    def test_incorrect_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(email="test", password="test123"),
                follow_redirects=True
            )
            self.assertIn(b'Please enter your email address.', response.data)
            self.assertIn('/login', request.url)

    def test_logout(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You have been logged out!', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to be logged in to access this page!', response.data)

    def test_get_by_id(self):
        with self.client:
            self.login('test@test.com', 'test123')
            self.assertTrue(current_user.id == 1)
            self.assertFalse(current_user.id == 20)

    def test_check_password(self):
        user = User.query.filter_by(email='test@test.com').first()
        self.assertTrue(check_password_hash(user.password_hash, 'test123'))
        self.assertFalse(check_password_hash(user.password_hash, 'foobar'))

class TestHost(BaseTestCase):

    def test_host_requires_login(self):
        response = self.client.get('/host', follow_redirects=True)
        self.assertIn(b'You need to be logged in to access this page!', response.data)

    def test_host_submission(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.post(
                '/host',
                data=dict(
                    name="Cube Day",
                    location="Cubicle",
                    date=datetime.date(2018, 5, 13),
                    events="rubikscube"
                ),
                follow_redirects=True
            )
            comp = Competition.query.filter_by(title="Cube Day").first()
            self.assertTrue(comp)

    def test_submission_on_manage(self):
        with self.client:
            self.login('test@test.com', 'test123')
            self.client.post(
                '/host',
                data=dict(
                    name="Cube Day",
                    location="Cubicle",
                    date=datetime.date(2018, 5, 13),
                ),
                follow_redirects=True
            )
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Cube Day', response.data)
            self.assertIn(b'2018-05-13', response.data)
            self.assertIn(b'Manage', response.data)



    def test_submission_matches_user(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.post(
                '/host',
                data=dict(
                    name="Cube Day",
                    location="Cubicle",
                    date=datetime.date(2018, 5, 13),
                    events="rubikscube"
                ),
                follow_redirects=True
            )
            comp = Competition.query.filter_by(title="Cube Day").first()
            self.assertTrue(comp.organizer_id == current_user.id)

class TestManage(BaseTestCase):

    def test_manage_requires_login(self):
        response = self.client.get('/manage', follow_redirects=True)
        self.assertIn(b'You need to be logged in to access this page!', response.data)

    def test_manage_displays_competition(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Test name', response.data)
            self.assertIn(b'Test location', response.data)
            self.assertIn(b'2017-12-31', response.data)
            self.assertIn(b'Manage', response.data)

    def test_manage_only_displays_currentuser_comps(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Test name', response.data)
            self.assertFalse(b'Cant view' in response.data)


    def test_manage_competitors_and_schedule(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage/1', content_type='html/text')
            self.assertIn(b'Firstname', response.data)
            self.assertIn(b'Competitor', response.data)
            self.assertIn(b'4x4x4 Cube', response.data)

    def test_manage_shows_organizer_edit_buttons(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage/1', content_type='html/text')
            self.assertIn(b'New Event', response.data)
            self.assertIn(b'Edit', response.data)
            self.assertIn(b'Delete', response.data)

    def test_manage_event_shows_info(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage/1/schedule/1', content_type='html/text')
            self.assertIn(b'11:00 AM - 12:00 PM', response.data)
            self.assertIn(b'Volunteers:', response.data)
            self.assertIn(b'Staff:', response.data)

    def test_manage_edit_event_displays_correctly(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage/1/schedule/1/edit', content_type='html/text')
            self.assertIn(b'Change Role', response.data)

class TestAnnouncement(BaseTestCase):
    def test_announcements_exist(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="mock@user.com", password="mock123"),
                follow_redirects=True
            )
            response = self.client.get('/manage/1/announcements', content_type='html/text')
            self.assertIn(b'Test announcement', response.data)
            self.assertIn(b'Test body', response.data)

    def test_comp_owner_can_post_announcement(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.get('/manage/1/announcements', content_type='html/text')
            self.assertIn(b'Title', response.data)
            self.assertIn(b'Body', response.data)

    def test_announcement_gets_posted(self):
        with self.client:
            self.login('test@test.com', 'test123')
            self.client.post(
                '/manage/1/announcements',
                data=dict(title="new post", body="new body"),
                follow_redirects=True
            )
            response = self.client.get('/manage/1/announcements', content_type='html/text')
            self.assertIn(b'new post', response.data)
            self.assertIn(b'new body', response.data)

    def test_incorrect_announcement_gets_posted(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.post(
                '/manage/1/announcements',
                data=dict(title="", body=""),
                follow_redirects=True
            )
            self.assertIn(b'Please enter a title', response.data)
            self.assertIn(b'Please enter a body', response.data)

class TestSchedule(BaseTestCase):
    def test_event_exist(self):
        with self.client:
            self.login('test@test.com', 'test123')

            response = self.client.get('/manage/1', content_type='html/text')
            self.assertIn(b'4x4x4 Cube', response.data)

    def test_event_is_created(self):
        with self.client:
            self.login('test@test.com', 'test123')
            response = self.client.post(
                '/manage/1/newevent',
                data=dict(
                    event="5x5x5 Cube",
                    event_round="Round 1",
                    start_time="11:00 AM",
                    end_time="12:00 PM"
                ),
                follow_redirects=True
            )
            self.assertIn(b'5x5x5 Cube', response.data)
            self.assertIn(b'Round 1', response.data)

if __name__ == '__main__':
    unittest.main()
