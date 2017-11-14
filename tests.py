from app import app, db
from flask_testing import TestCase
from flask import request
from werkzeug.security import check_password_hash

import unittest
import datetime

from flask_login import current_user
from app.models import User, Competition

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User("Firstname", "Lastname", "test@test.com", "test123")
        comp = Competition(user.wca_id, "Test name", "Test location", datetime.date(2017, 12, 31))
        db.session.add(user)
        db.session.add(comp)
        db.session.commit()

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


if __name__ == '__main__':
    unittest.main()
