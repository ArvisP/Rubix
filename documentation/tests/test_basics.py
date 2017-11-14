from flask import request
from base import BaseTestCase

import unittest
from flask.ext.sqlalchemy import SQLAlchemy
from app import app

# models
from User.models import *
from Competitions.models import *

class FlaskTestCase(unittest.TestCase):
    # Ensure that flask was set up correctly
    def test_index(self):
        # the test client is what we use to create a test, mocking the functionality of our current app that we can use the send request to and then test the responses all outside the scope of our mani app
        tester = app.test_client(self)
        # we're using the unit test library to call the login route
        response = tester.get('/login', content_type='html/text')
        # then we're checking the response status code and ensuring that it equals 200
        self.assertEqual(response.status_code, 200)

    # Ensure the main page requires login
    def test_main_route_requires_login(self):
        tester = app.test_client(self)
        response = tester.get('/', follow_redirects=True)
        self.assertTrue(b'You need to login first.' in response.data)
    
class UserViewsTests(BaseTestCase):

    # Ensure that the login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login')
        self.assertIn(b'Please login', response.data)

    # Ensure login behaves correctly with correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'You were logged in', response.data)
            self.assertTrue(current_user.name == "admin")
            self.assertTrue(current_user.is_active())

    # Ensure login behaves correctly with incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login',
            data=dict(username="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid username or password.', response.data)

    # Ensure logout behaves correctly
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out', response.data)
            self.assertFalse(current_user.is_active())

    # Ensure that logout page requires user login
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    # Ensure that posts show up on the main page (web scraping results will be displayed on the main index page)

# Each test should only test one piece of functionality        

if __name__ == 'main':
    unittest.main()

 
 # setUp and Teardown are sections of this class that always called the beginning and end of each test
 # setUp will involve creating a temporary database, we dont use the main database, we create an alternate one, so we can use dummy data to test the code
 #  