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
stathat.init_app(app)  # or stathat = StatHat(app)

toolbar = DebugToolbarExtension(app)
