from app import app, db
from flask import request
from werkzeug.security import check_password_hash

import os.path as op
import unittest
import datetime
import os


from flask_testing import TestCase
from flask_login import current_user
from app.models import User, Competition, Announcement, Event, EventUserLink
from bs4 import BeautifulSoup

class BaseTestCase(TestCase):
    '''
    Initializes the app
    '''
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app
    '''
    Creates the database and adds data to the database
    '''
    def setUp(self):
        self.dir = os.path.dirname(
            os.path.abspath(__file__))
        self.app = rubix.app.test_client()
        self.response = self.client.app.get("/")
        self.soup = BeautifulSoup(self.response.data,
                                  'html.parser')

        db.create_all()
        db.session.add(User("Firstname", "Lastname", "test@test.com", "test123"))
        db.session.add(User("Mock", "User", "mock@user.com", "mock123"))
        db.session.add(User("new", "User", "new@user.com", "new123"))
        db.session.add(User("Competitor", "Jones", "comp@jones.com", "comp123"))
        db.session.add(User("delegate", "DeeDee", "delegatetest@test.com", "1234567890"))
        user = User.query.filter_by(email="test@test.com").first()
        user1 = User.query.filter_by(email="new@user.com").first()
        user2 = User.query.filter_by(email="comp@jones.com").first()
        delegateuser = User.query.filter_by(email='delegatetest@test.com',credentials=2).first()

        db.session.add(Competition(user.id, "Test name", "Test location", "Test City", "Test State", "10031", datetime.date(2017, 12, 31)))
        db.session.add(Competition(20, "Cant view", "Cant view", "New York", "NY", "10031", datetime.date(2017, 12, 31)))
        comp = Competition.query.filter_by(comp_id=1).first()
        comp.approved = True
        comp20 = Competition.query.filter_by(organizer_id=20).first()

        announce1 = Announcement(comp.comp_id, user.id, "Test announcement", "Test body")
        announce2 = Announcement(comp20.comp_id, 2, "Can i see this?", "maybe")
        db.session.add(announce1)
        db.session.add(announce2)

        event1 = Event('Rubik\'s Cube', 'Round 1', datetime.time(11, 0, 0), datetime.time(12, 0, 0))
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

class TestBasic(BaseTestCase):
    '''Ensure that flask was set up correctly'''
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

class TestUnitRubix(BaseTestCase):
    def test_check_rubix_config(self):
        file_exists = op.exists(op.join(self.dir,'config.py'))
        self.assertTrue(file_exists)

    def test_check_rubix_createdata(self):
        file_exists = op.exists(op.join(self.dir,'db_create_data.py'))
        self.assertTrue(file_exists)

    def test_check_rubix_createdb(self):
        file_exists = op.exists(op.join(self.dir,'db_create.py'))
        self.assertTrue(file_exists)

    def test_check_rubix_run(self):
        file_exists = op.exists(op.join(self.dir,'run.py'))
        self.assertTrue(file_exists)


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
            response = self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
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
            self.assertTrue(comp.organizer_id == current_user.id)

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


    def test_manage_info_competitors(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
        response = self.client.get('/manage/1', content_type='html/text')
        self.assertIn(b'Firstname', response.data)
        self.assertIn(b'Competitor', response.data)

    def test_manage_shows_vol_staff(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="comp@jones.com", password="comp123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'Volunteers:', response.data)
            self.assertIn(b'Staff:', response.data)
    
    def test_manage_accept_competition(self):
        with self.client:
            self.client

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
            response = self.client.get('/manage/1/announcements', content_type='html/text')
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

class TestSchedule(BaseTestCase):
    def test_event_exist(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )

            response = self.client.get('/manage/1/schedule', content_type='html/text')
            self.assertIn(b'Rubik\'s Cube', response.data)

    def test_event_is_created(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.post(
                '/manage/1/newevent',
                data=dict(
                    event="4x4x4 Cube",
                    event_round="Round 1",
                    start_time="11:00 AM",
                    end_time="12:00 PM"
                ),
                follow_redirects=True
            )
            self.assertIn(b'4x4x4 Cube', response.data)
            self.assertIn(b'Round 1', response.data)


class TestCompetitionsView(BaseTestCase):
    def test_comp_info_correctly_displays(self):
        response = self.client.get('/competitions/1', content_type='html/text')
        self.assertIn(b'Test name', response.data)
        self.assertIn(b'Firstname', response.data)
        self.assertIn(b'Competitor', response.data)


    def test_comp_announcements(self):
        response = self.client.get('/competitions/1/announcements', content_type='html/text')
        self.assertIn(b'Test announcement', response.data)


    def test_comp_schedule(self):
        response = self.client.get('/competitions/1/schedule', content_type='html/text')
        self.assertIn(b'Rubik\'s Cube', response.data)
        self.assertIn(b'Round 1', response.data)

    def test_unregistered_user_can_register(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="mock@user.com", password="mock123"),
                follow_redirects=True
            )

            response = self.client.get('/competitions/1', content_type='html/text')
            self.assertIn(b'Register', response.data)

    def test_registered_user_cannot_register(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1', content_type='html/text')
            self.assertFalse(b'Register' in response.data)


    def test_event_can_be_registered(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="mock@user.com", password="mock123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'Register Event', response.data)


    def test_cannot_volunteer_unless_registered(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="mock@user.com", password="mock123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertFalse(b'Request to Volunteer' in response.data)

    def test_user_can_volunteer_if_registered(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="new@user.com", password="new123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'Request to Volunteer', response.data)

    def test_user_is_volunteering(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="comp@jones.com", password="comp123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'You are volunteering in this event as a Judge', response.data)

    def test_comp_shows_vol_staff(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'Volunteers:', response.data)
            self.assertIn(b'Staff:', response.data)

    def test_volunteer_approved_exists(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'Competitor', response.data)
            self.assertIn(b'Jones', response.data)
            self.assertIn(b'Judge', response.data)
            # self.assertFalse(b'new' in response.data)
            # self.assertFalse(b'User' in response.data)


    def test_staff_approved_exists(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="test@test.com", password="test123"),
                follow_redirects=True
            )
            response = self.client.get('/competitions/1/schedule/1', content_type='html/text')
            self.assertIn(b'New', response.data)
            self.assertIn(b'User', response.data)
            self.assertIn(b'Scrambler', response.data)
            # self.assertFalse(b'Competitor' in response.data)
            # self.assertFalse(b'Jones' in response.data)

class TestUserProfile(BaseTestCase):
    # this tests to check that the name in the tab is the same as the one we said so here, which it is....but not working
    # error: AttributeError: 'Flask' object has no attribute 'get'
    def test_user_profile_tab_name(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="delegatetest@test.com", password="1234567890"),
                follow_redirects=True
            )
            response = self.client.get('/profile', content_type='html/text')
            self.client.assertEqual("current_user.first_name current_user.last_name",self.soup.title.text)

    def test_user_profile_header(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(email="delegatetest@test.com", password="1234567890"),
                follow_redirects=True
            )
            response = self.client.get('/profile', content_type='html/text')
            self.client.assertEqual("current_user.first_name current_user.last_name",self.soup.h1.text.strip())
    
class TestUnitApp(BaseTestCase):
    def test_check_routes_file(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          '__init__.py'))
        self.assertTrue(file_exits)

    def test_check_routes(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'routes.py'))
        self.assertTrue(file_exits)
    
    def test_check_models(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'models.py'))
        self.assertTrue(file_exits)
    
    def test_check_forms(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'forms.py'))
        self.assertTrue(file_exits)
    
    def test_check_chat(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'chat.py'))
        self.assertTrue(file_exits)
    # this is the checks for the profile layout, this layout is used by both regular users and delegates
    def test_check_profile_layout(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          'profile-layout.html'))
        self.assertTrue(file_exits)
    
    def test_check_profile_page(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          'user_profile.html'))
        self.assertTrue(file_exits)
    
    def test_check_delegate_page(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          'delegate_profile.html'))
        self.assertTrue(file_exits)
    
    def test_check_landing_page(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          'landing_page.html'))
        self.assertTrue(file_exits)

    def test_check_layout(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          'layout.html'))
        self.assertTrue(file_exits)

    def test_check_404(self):
        file_exits = op.exists(op.join(self.dir,
                          'app',
                          'templates',
                          '404.html'))
        self.assertTrue(file_exits)

class TestUnitProject(BaseTestCase):
    # this __init__.py file is for the entire projects folder
    def test_check_init(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          '__init__.py'
                          ))
        self.assertTrue(file_exits)
    # this __init__.py file is for the directory: competitions
    def test_check_competitions_init(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          '__init__.py'
                          ))
        self.assertTrue(file_exits)
    
    def test_check_competitions_views(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'views.py'
                          ))
        self.assertTrue(file_exits)

    def test_check_competitions_announcements(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_announcements.html'))
        self.assertTrue(file_exits)
    
    def test_check_competitions_event(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_event.html'
                          ))
        self.assertTrue(file_exits)

    def test_check_competitions_info(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_info.html'
                          ))
        self.assertTrue(file_exits)
    
    def test_check_competitions_nav(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_nav.html'
                          ))
        self.assertTrue(file_exits)

    def test_check_competitions_register(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_register.html'
                          ))
        self.assertTrue(file_exits)

    def test_check_competitions_schedule(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'comp_schedule.html'
                          ))
        self.assertTrue(file_exits)

    def test_check_competitions_file(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'competitions',
                          'templates',
                          'competitions.html'
                          ))
        self.assertTrue(file_exits)
    # HOST directory
    def test_check_host_init(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'host',
                          '__init__.py'))
        self.assertTrue(file_exits)

    def test_check_host_view(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'host',
                          'views.py'))
        self.assertTrue(file_exits)

    def test_check_host_file(self):
        file_exits = op.exists(op.join(self.dir,
                          'project',
                          'host',
                          'templates'
                          'host.html'))
        self.assertTrue(file_exits)
    #manage directory
    def test_check_manage_init(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            '__init__.py'))
        self.assertTrue(file_exists)

    def test_check_manage_view(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'views.py'))
        self.assertTrue(file_exists)

    def test_check_manage_announcements(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'announcements.html'))
        self.assertTrue(file_exists)

    def test_check_manage_competition_layout(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'competition_layout.html'))
        self.assertTrue(file_exists)

    def test_check_manage_compnavbar(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'competition_navbar.html'))
        self.assertTrue(file_exists)

    def test_check_manage_competition(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'competition.html'))
        self.assertTrue(file_exists)

    def test_check_manage_competitors(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'competitors.html'))
        self.assertTrue(file_exists)

    def test_check_manage_details(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'details.html'))
        self.assertTrue(file_exists)

    def test_check_manage_edit(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'edit.html'))
        self.assertTrue(file_exists)

    def test_check_manage_event(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'event.html'))
        self.assertTrue(file_exists)

    def test_check_manage_file(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'manage.html'))
        self.assertTrue(file_exists)

    def test_check_manage_newevent(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'newevent.html'))
        self.assertTrue(file_exists)

    def test_check_manage_schedule(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'manage',
                            'templates',
                            'schedule.html'))
        self.assertTrue(file_exists)
    # User directory
    def test_check_manage_init(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'users',
                            '__init__.py'))
        self.assertTrue(file_exists)

    def test_check_manage_views(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'users',
                            'views.py'))
        self.assertTrue(file_exists)

    def test_check_user_login(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'users',
                            'templates',
                            'login.html'))
        self.assertTrue(file_exists)

    def test_check_user_signup(self):
        file_exists = op.exists(op.join(self.dir,
                            'project',
                            'users',
                            'templates',
                            'signup.html'))
        self.assertTrue(file_exists)

if __name__ == '__main__':
    unittest.main()
