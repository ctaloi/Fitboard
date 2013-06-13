from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask_debugtoolbar import DebugToolbarExtension
from flask_stathat import StatHat
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object('config')

stathat = StatHat()
stathat = StatHat(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

heroku = Heroku(app)

toolbar = DebugToolbarExtension(app)

db = SQLAlchemy(app)

handler = RotatingFileHandler('fitboard.log', maxBytes=10000, backupCount=1)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)
