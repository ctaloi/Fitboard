
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