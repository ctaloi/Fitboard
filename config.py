import os

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# SECRET_KEY = os.environ['SECRET_KEY']

SECRET_KEY = '6Nue]A=U+3t%4@af4U+E'
SQLALCHEMY_DATABASE_URI = 'postgres://qwcucsqoeopfam:-3CwkaK4_nkCmFqyly0Rkd2Po8@ec2-23-21-129-229.compute-1.amazonaws.com:5432/d9kajj9pmpem7c'

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS = False
