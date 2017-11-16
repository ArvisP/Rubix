from app import app, db
from flask import request
from werkzeug.security import check_password_hash

import unittest
import datetime

from flask_testing import TestCase
from flask_login import current_user
from app.models import User, Competition, Announcement

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
        user = User.query.filter_by(email="test@test.com").first()

        db.session.add(Competition(user.wca_id, "Test name", "Test location", datetime.date(2017, 12, 31)))
        db.session.add(Competition(20, "Cant view", "Cant view", datetime.date(2017, 12, 31)))
        comp = Competition.query.filter_by(comp_id=1).first()

        announce = Announcement(comp.comp_id, user.wca_id, "Test announcement", "Test body")

        db.session.add(announce)
        db.session.commit()

    '''
    Drops all tables from the database
    '''
    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
            self.assertIn(b'You have signed up! Please log in!', response.data)
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
            response = self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            self.assertIn(b'Logged in', response.data)
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
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You have been logged out!', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to be logged in to access this page!', response.data)

    def test_get_by_id(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password='test123'),
                follow_redirects=True
            )
            self.assertTrue(current_user.wca_id == 1)
            self.assertFalse(current_user.wca_id == 20)

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
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
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
            self.assertIn(b'Cube Day has been created!', response.data)

    def test_submission_on_manage(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            self.client.post(
                '/host',
                data=dict(
                    name="Cube Day",
                    location="Cubicle",
                    date=datetime.date(2018, 5, 13),
                    events="rubikscube"
                ),
                follow_redirects=True
            )
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Cube Day', response.data)
            self.assertIn(b'Cubicle', response.data)
            self.assertIn(b'2018-05-13', response.data)
            self.assertIn(b'Manage', response.data)



    def test_submission_matches_user(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
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
            self.assertTrue(comp.organizer_id == current_user.wca_id)

class TestManage(BaseTestCase):

    def test_manage_requires_login(self):
        response = self.client.get('/manage', follow_redirects=True)
        self.assertIn(b'You need to be logged in to access this page!', response.data)

    def test_manage_displays_competition(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Test name', response.data)
            self.assertIn(b'Test location', response.data)
            self.assertIn(b'2017-12-31', response.data)
            self.assertIn(b'Manage', response.data)

    def test_manage_only_displays_currentuser_comps(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/manage', content_type='html/text')
            self.assertIn(b'Test name', response.data)
            self.assertFalse(b'Cant view' in response.data)

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
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/manage/1/announcements', content_type='html/text')
            self.assertIn(b'Title', response.data)
            self.assertIn(b'Body', response.data)

    def test_announcement_gets_posted(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            self.client.post(
                '/manage/1/announcements',
                data=dict(title="new post", body="new body"),
                follow_redirects=True
            )
            response = self.client.get('manage/1/announcements', content_type='html/text')
            self.assertIn(b'new post', response.data)
            self.assertIn(b'new body', response.data)

    def test_incorrect_announcement_gets_posted(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.post(
                '/manage/1/announcements',
                data=dict(title="", body=""),
                follow_redirects=True
            )
            self.assertIn(b'Please enter a title', response.data)
            self.assertIn(b'Please enter a body', response.data)

if __name__ == '__main__':
    unittest.main()
