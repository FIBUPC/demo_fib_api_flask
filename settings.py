# Server config

DEBUG = True

# It's important to change this before deploying
SECRET_KEY = 'development'

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'development'

class TestingConfig(Config):
    TESTING = True