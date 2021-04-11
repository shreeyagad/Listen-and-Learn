import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Different environments for the app to run in

class Config(object):
  DEBUG = False
  CSRF_ENABLED = True
  CSRF_SESSION_KEY = "secret"
  SECRET_KEY = "not_this"
  SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
  SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
  SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True
