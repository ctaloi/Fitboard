import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

DEBUG_TB_INTERCEPT_REDIRECTS = False

STATHAT_EZ_KEY = 'ctaloi@gmail.com'
STATHAT_USE_GEVENT = False

DEBUG = True
