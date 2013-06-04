from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_stathat import StatHat
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

stathat = StatHat()
stathat = StatHat(app)

toolbar = DebugToolbarExtension(app)

ADMINS = ['ctaloi@gmail.com']
# if not app.debug:
mail_handler = SMTPHandler('127.0.0.1',
                           'fitboard@fitboard.me',
                           ADMINS, 'FitBoard Failed')
mail_handler.setLevel(logging.ERROR)
app.logger.addHandler(mail_handler)