WTF_CSRF_ENABLED = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class HerokuDeployConfig(object):
    SECRET_KEY = 'thisPasswordIsSoDarnAmazinglyStrong123!'
<<<<<<< HEAD
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
=======
#    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
>>>>>>> 320452e407447b292fda0f8b655ae9eddd4f0c0a
    SQLALCHEMY_TRACK_MODIFICATIONS = False
