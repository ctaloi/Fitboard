import os

# ---- choose DB ----
# if sqlite

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# else
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# get secret key for session
SECRET_KEY = os.environ['SECRET_KEY']

# stathat config
DEBUG = False
STATHAT_EZ_KEY = 'ctaloi@gmail.com'
STATHAT_USE_GEVENT = False

# flask-toolbar config
DEBUG_TB_INTERCEPT_REDIRECTS = False
