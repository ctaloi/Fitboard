from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import os
import chartkick

app = Flask(__name__, static_folder=chartkick.js(), static_url_path='/static')
# app = Flask(__name__)
app.jinja_env.add_extension("chartkick.ext.charts")

app.config.from_object('config')

heroku = Heroku(app)

toolbar = DebugToolbarExtension(app)

db = SQLAlchemy(app)

mail = Mail(app)

if os.environ.get('HEROKU') is True:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('FITBOARD-START-HEROKU')

else:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('fitboard.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('FITBOARD-START')
