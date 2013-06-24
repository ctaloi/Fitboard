import os

DEBUG = True

# ---- choose DB ----
# if sqlite

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# else
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# get secret key for session
SECRET_KEY = os.environ['SECRET_KEY']

# flask-toolbar config
DEBUG_TB_INTERCEPT_REDIRECTS = False

# mail config
MAIL_SERVER = "smtp.gmail.com"
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_DEFAULT_SENDER = os.environ['MAIL_USERNAME']
MAIL_DEBUG = False
