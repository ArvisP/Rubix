from app import app
from flask_testing import TestCase

import unittest

from flask_login import current_user
from app.models import User, Competition

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User("Firstname", "Lastname", "test@test.com", "test123")
        comp = Competition(user.wca_id, "Test name", "Test location", "12/31/2017")
        db.session.add(user)
        db.session.add(comp)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class RubixTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertIn(b'Log in', response.data)

    def test_login_page_loads(self):
        response = self.client.post(
            '/login',
            data=dict(email="test@test.com", password="test123"),
            follow_redirects=True
        )
        self.assertTrue(current_user.is_authenticated)


if __name__ == '__main__':
    unittest.main()
