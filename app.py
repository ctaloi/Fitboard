from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_stathat import StatHat
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('SECRETS', silent=True)

stathat = StatHat()
stathat.init_app(app)  # or stathat = StatHat(app)

toolbar = DebugToolbarExtension(app)

handler = RotatingFileHandler('fitboard.log', maxBytes=10000, backupCount=1)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

db = SQLAlchemy(app)
