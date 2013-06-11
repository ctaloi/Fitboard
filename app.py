from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import logging
from logging import Formatter, StreamHandler

app = Flask(__name__)
app.config.from_object('config')

toolbar = DebugToolbarExtension(app)

# handler = RotatingFileHandler('fitboard.log', maxBytes=10000, backupCount=1)
# handler.setFormatter(Formatter(
#     '%(asctime)s %(levelname)s: %(message)s '
#     '[in %(pathname)s:%(lineno)d]'
# ))
# handler.setLevel(logging.WARNING)
# app.logger.addHandler(handler)

st_logger = StreamHandler()
st_logger.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
st_logger.setLevel(logging.INFO)
app.logger.addHandler(st_logger)

db = SQLAlchemy(app)
