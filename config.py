import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # environment variables setup for SQLAlchemy databases
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI =  os.environ.get("TEST_DATABASE_URL") or 'sqlite:///' + os.path.join(basedir, 'test.db')