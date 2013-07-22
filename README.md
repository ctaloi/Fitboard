# About Fitboard

[Fitboard.me](http://fitboard.me) is a webapp built to connect the [Fitbit API](http://dev.fitbit.com/) to [Panic's Status Board](https://panic.com/statusboard/) iPad application.  Fitboard is free for anyone to use at [Fitboard.me](http://fitboard.me) or you can fork the repo and build your own.

The source for Fitboard is open - please contribute.

Fitboard allows you to visualize

- Steps
- Calories
- Distance
- Floors
- Active Score
- Minutes Asleep
- Sleep Efficiency
- Times Awakened
- Minutes Sedentary
- Minutes Lightly Active
- Minutes Fairly Active
- Minutes Very Active


And a multi point graph showing

- Minutes Sedentary
- Minutes Lightly Active
- Minutes Fairly Active
- Minutes Very Active

Over

- 1 Day
- 7 Days
- 1 Month
- 3 Months
- 6 Months
- 1 Year
- Max

In Status Board on your iPad

Fitboard depends heavily on the following **awesome** Python packages:

- [Python FitBit API Client](https://github.com/orcasgit/python-fitbit)
- [Flask](http://flask.pocoo.org/)

You can see the full list of packages in [requirements.txt](https://github.com/ctaloi/Fitboard/blob/master/requirements.txt)


**********

# Building Fitboard

You should be able to deploy Fitboard locally, to a VPS or on Heroku with minimal configuration changes.

### Local Build

Use [Virtualenv Wrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) to manage virtual environments

Create a new virtual environment

    mkvirtualenv fitboard

### Clone fitboard

    cd ~/Projects
    git clone https://github.com/ctaloi/Fitboard.git

### Install Fitboard Requirements

    cd ~/Projects/Fitboard
    workon fitboard
    pip -r install requirements.txt

### Use SQLite

Set your config.py file for local SQLite

    # if sqlite, uncomment the next two lines
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    # else
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

### Get Connected

In order to talk to the Fitbit API you need to [sign up](https://dev.fitbit.com/apps/new) and obtain a key and secret.

Completing the registration request is easy.

- Default access type: Read-Only
- Application Type: Browser

Save your CONSUMER_KEY and CONSUMER_SECRET

## Heroku Deployment

Install [Heroku Toolbelt](https://toolbelt.heroku.com/)

Follow the Getting started with Flask and Heroku [guide](https://devcenter.heroku.com/articles/python) for setting up your Heroku Deployment

Add Postgres addon

    heroku addons:add heroku-postgresql:dev

Promote the database

    heroku pg:promote HEROKU_POSTGRESQL_TEAL_URL

This sets up Postgres and sets the heroku config DATABASE_URL for us.  To create and populate the database table we need to use a heroku python shell

    heroku run python
    >>> from main import db
    >>> db.create_all()

You can use this Postgres instance locally or deployed

## Standalone Deployment

Flask can also run under a standalone WSGI container - [more detail and options](http://flask.pocoo.org/docs/deploying/wsgi-standalone/)

I've tested with the following stack:

- [Flask](http://flask.pocoo.org/)
- [Gunicorn](http://gunicorn.org/)
- [NGINX](http://nginx.org/)
- [Supervisor](https://pypi.python.org/pypi/supervisor)

### Summary of standalone configuration

Basically - Supervisor starts Gunicorn who starts the fitboard app

#### Supervisor

config: /etc/supervisor/conf.d/fitboard.conf

    [program:gunicorn]
    command=/home/fitboard/.virtualenvs/Fitboard/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
    directory=/home/fitboard/fitboard
    user=fitboard
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=CONSUMER_KEY="XXX",CONSUMER_SECRET="XXX",DATABASE_URL="XXX",SECRET_KEY="XXX"

#### NGINX

config: /etc/nginx/sites-available/fitboard (symlink in sites-enabled)

    server {
        listen 80;
        server_name fitboard.me;
        access_log  /var/log/nginx/fitboard.log;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
      }

#### Gunicorn

Gunicorn is configured in the supervisor config file

## Start Fitboard

### Local

- Edit config.py and set debug to True

To start Fitboard running under Flask debug mode (local - non production) you need to setup your environmental variables using the CONSUMER_KEY and CONSUMER_SECRET provided by Fitbit and other 'secure' variables of your deployment.

I have a shell script which runs the following

    export CONSUMER_KEY=
    export CONSUMER_SECRET=
    export DATABASE_URL=
    export SECRET_KEY=
    export MAIL_USERNAME=
    export MAIL_PASSWORD=
    ./python main.py

### Heroku

Set your variables using the Heroku CLI

    heroku config:set SECRET_KEY=
    heroku config:set CONSUMER_KEY=
    heroku config:set CONSUMER_SECRET=
    heroku config:set MAIL_USERNAME=
    heroku config:set MAIL_PASSWORD=
    heroku config:set DATABASE_URL=

### Standalone

Your environmental variables are called in the your supervisor config

config: /etc/supervisor/conf.d/fitboard.conf

    [program:gunicorn]
    command=/home/chris/Envs/fitboard/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
    directory=/home/chris/Projects/Fitboard
    user=chris
    autostart=true
    autorestart=true
    redirect_stderr=True
    environment=CONSUMER_KEY="XXX",CONSUMER_SECRET="XXX",DATABASE_URL="XXX",SECRET_KEY="XXX"

    service nginx restart
    service supervisor restart

Supervisor will trigger Gunicorn and Fitboard
















