
# Building fitboard.me

You should be able to depoly Fitboard locally, to a VPS or on Heroku with minimal configuration changes

## Local Prep

### Create a new virtalenv

Use [Virtualenv Wrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) to manage virtual environments

    mkvirtualenv fitboard

### Clone fitboard

    cd ~/Projects
    git clone https://github.com/ctaloi/Fitboard.git

### Install python tools

    cd ~/Projects/Fitboard
    workon fitboard
    pip -r install requirments.txt

### If using Heroku

- Install [Heroku Toolbelt](https://toolbelt.heroku.com/)

## Choose a database

I've tested Fitboard with SQLite and Postgres, both work well and using SQLAlchemy makes it easy.

### If using Heroku

Heroku does not support SQLite so I am using Postgres

Add Postgres addon

    heroku addons:add heroku-postgresql:dev

Promote the database

    heroku pg:promote HEROKU_POSTGRESQL_TEAL_URL


This sets up Postgres and sets the heroku config DATABASE_URL for us.  To create and populate the database table we need to use a heroku python shell

    heroku run python
    >>> from main import db
    >>> db.create_all()

You can use this Postgres instance locally or deployed

You shouldn't need to do anything else if you are using SQLite

## Configure the app

In order to talk to the Fitbit API you need to [register](https://dev.fitbit.com/apps/new) your app and obtain a consumer key and secret.

Completing the registration request is easy.

- Default access type: Read-Only
- Application Type: Browser

Note the CONSUMER_KEY and CONSUMER_SECRET


















