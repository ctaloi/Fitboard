
# Building fitboard.me

## Create a new virtalenv

I use [Virtualenv Wrapper](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) to manage my virtual environments

    mkvirtualenv fitboard_me

## Get Python ready

    pip install -r requirements.txt

This installs the following:

    Flask==0.9
    Flask-DebugToolbar==0.8.0
    Flask-OAuth==0.12
    Flask-SQLAlchemy==0.16
    Jinja2==2.7
    MarkupSafe==0.18
    SQLAlchemy==0.8.1
    Werkzeug==0.8.3
    blinker==1.2
    distribute==0.6.45
    fitbit==0.0.2
    httplib2==0.8
    itsdangerous==0.21
    oauth2==1.5.211
    python-dateutil==1.5
    requests==0.14.0
    wsgiref==0.1.2


# Init DB


# On heroku, add

heroku addons:add heroku-postgresql:dev

    Adding heroku-postgresql:dev on fitboard-me... done, v15 (free)
    Attached as HEROKU_POSTGRESQL_TEAL_URL
    Database has been created and is available
     ! This database is empty. If upgrading, you can transfer
     ! data from another database with pgbackups:restore.
    Use `heroku addons:docs heroku-postgresql:dev` to view documentation.

(fitboard_me)imac27:fitboard_me Chris$ heroku pg:promote HEROKU_POSTGRESQL_TEAL_URL

    Promoting HEROKU_POSTGRESQL_TEAL_URL to DATABASE_URL... done

Enter to get an interactive python shell

    heroku run python
    >>> from main import db
    >>> db.create_all()


