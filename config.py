import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = os.environ['DEBUG_MODE']

STATHAT_EZ_KEY = 'ctaloi@gmail.com'
STATHAT_USE_GEVENT = False

DEBUG_TB_INTERCEPT_REDIRECTS = False
