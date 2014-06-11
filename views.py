import fitbit
from flask import render_template, flash, redirect, session, url_for, request, jsonify, send_from_directory
from app import app, db, mail, Message
from models import User
from random import choice
from flask_oauthlib.client import OAuth
from stathat import StatHat
import os
import humanize
import dateutil.parser

MY_STATHAT_USER = os.environ.get('STATHAT_USER')
MY_CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
MY_CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

# Setup
# ----------------------------
oauth = OAuth()
fitbit_app = oauth.remote_app(
    'fitbit',
    base_url='https://api.fitbit.com',
    request_token_url='https://api.fitbit.com/oauth/request_token',
    access_token_url='https://api.fitbit.com/oauth/access_token',
    authorize_url='https://www.fitbit.com/oauth/authorize',
    consumer_key=MY_CONSUMER_KEY,
    consumer_secret=MY_CONSUMER_SECRET
)


# Logging
# ----------------------------

def email_log(message):
    msg = Message("%s Notice Fitboard" % (message),
                  recipients=["ctaloi@gmail.com"])
    msg.body = "NOTICE %s \n Logile Attached \n" % (message)
    with app.open_resource("fitboard.log") as fp:
        msg.attach("fitboard.log", "text/plain", fp.read())
    mail.send(msg)
    return


def email_alert(message):
    msg = Message("%s Notice Fitboard" % (message),
                  recipients=["ctaloi@gmail.com"])
    msg.body = "NOTICE %s \n " % (message)
    mail.send(msg)
    return


def stat_log(statistic):
    stats = StatHat(MY_STATHAT_USER)
    app.logger.info(statistic)
    try:
        stats.count(statistic, 1)
    except Exception:
        app.logger.info('push to stathat failed')
        pass


# Routes
# ----------------------------

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    app.logger.info('404')
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('intro.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@fitbit_app.tokengetter
def get_fitbit_app_token(token=None):
    return session.get('fitbit_app_token')


@app.route('/login')
def login():
    """ Start login process
    """
    # email_alert('NEW LOGIN')
    stat_log('Fitboard Login Counter')
    return fitbit_app.authorize(
        callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))


@app.route('/oauth_authorized')
@fitbit_app.authorized_handler
def oauth_authorized(resp):
    """ Authorize using OAUTH """
    next_url = request.args.get('next') or url_for('charts')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    # print request
    # print resp

    user_id = resp['encoded_user_id']
    user_key = resp['oauth_token']
    user_secret = resp['oauth_token_secret']

    session['fitbit_keys'] = (
        user_id, user_key, user_secret)  # add session cookie
    active_user = User(user_id, user_key, user_secret)
    check_user = User.query.filter_by(user_id=user_id).first()

    if check_user is None:
        db.session.add(active_user)
        db.session.commit()

    session['user_profile'] = get_user_profile(user_id)
    session['device_info'] = get_device_info(user_id)

    return redirect(url_for('charts'))


@app.route('/u/<user_id>/drop')
def drop_user(user_id):
    """ Drop user from databaase """
    app.logger.info('delete,request to delete %r' % user_id)

    user = User.query.filter_by(user_id=user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    check_user = User.query.filter_by(user_id=user_id).first()

    if check_user is None:
        flash('Successfully Deleted Account')
        session.pop('fitbit_keys', None)
        session.pop('user_profile', None)
        session.pop('device_info', None)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """ Logout pops session cookie """
    session.pop('fitbit_keys', None)
    session.pop('user_profile', None)
    return redirect(url_for('index'))


@app.route('/dash/<user_id>/')
@app.route('/dash/<user_id>')
def get_dashboard(user_id):
    """ Function to build a simple table showing various status """
    profile = get_user_profile(user_id)
    device = get_device_info(user_id)
    steps = get_activity(
        user_id, 'steps', period='1d', return_as='raw')[0]['value']
    return render_template('dash.html', device=device, steps=steps, profile=profile)


@app.route('/u/<user_id>/<resource>/<period>')
def get_activity(user_id, resource, period='1w', return_as='json'):
    """ Function to pull data from Fitbit API and return as json or raw specific to activities """
    global dash_resource
    app.logger.info('resource, %s, %s, %s, %s, %s' %
                    (user_id, resource, period, return_as, request.remote_addr))
    stat_log('Fitboard Calls')
    ''' Use  API to return resource data '''

    slash_resource = 'activities/' + resource

    colors = (
        'yellow',
        'green',
        'red',
        'blue',
        'mediumGray',
        'aqua',
        'orange',
        'lightGray')

    datasequence_color = choice(colors)

    if period in ('1d', '1w', '1m'):
        graph_type = 'bar'
    else:
        graph_type = 'line'

    # Activity Data
    if resource in ('distance',
                    'steps',
                    'floors',
                    'calories',
                    'elevation',
                    'minutesSedentary',
                    'minutesLightlyActive',
                    'minutesFairlyActive',
                    'minutesVeryActive',
                    'activeScore',
                    'activityCalories'):
        slash_resource = 'activities/' + resource
        dash_resource = 'activities-' + resource

    # Sleep Data
    if resource in ('startTime',
                    'startTime',
                    'timeInBed',
                    'minutesAsleep',
                    'awakeningsCount',
                    'minutesAwake',
                    'minutesToFallAsleep',
                    'minutesAfterWakeup',
                    'efficiency'):
        slash_resource = 'sleep/' + resource
        dash_resource = 'sleep-' + resource

    if resource in ('weight',
                    'bmi',
                    'fat'):
        slash_resource = 'body/' + resource
        dash_resource = 'body-' + resource

    the_data = get_connector(user_id).time_series(
        slash_resource, base_date='today', period=period)[dash_resource]

    if return_as == 'raw':
        return the_data
    if return_as == 'json':
        return jsonify(output_json(the_data, resource, datasequence_color, graph_type))


@app.route('/u/summary/<user_id>/<period>')
def get_levelsummary(user_id, period):
    """ Function to build a four point graph summarizing activities """

    app.logger.info('summary, summary, %s, %s, %s' %
                    (user_id, period, request.remote_addr))

    if period in ('1d', '1w'):
        g_type = 'bar'
    else:
        g_type = 'line'

    minutesSedentary = get_activity(
        user_id, 'minutesSedentary', period=period, return_as='raw')
    minutesLightlyActive = get_activity(
        user_id, 'minutesLightlyActive', period=period, return_as='raw')
    minutesFairlyActive = get_activity(
        user_id, 'minutesFairlyActive', period=period, return_as='raw')
    minutesVeryActive = get_activity(
        user_id, 'minutesVeryActive', period=period, return_as='raw')

    datasequences = []

    ms = []
    ml = []
    mf = []
    mv = []

    for x in minutesSedentary:
        ms.append({'title': x['dateTime'], 'value': float(x['value']) - 480})
    for x in minutesLightlyActive:
        ml.append({'title': x['dateTime'], 'value': float(x['value'])})
    for x in minutesFairlyActive:
        mf.append({'title': x['dateTime'], 'value': float(x['value'])})
    for x in minutesVeryActive:
        mv.append({'title': x['dateTime'], 'value': float(x['value'])})

    datasequences.append({
        "title": 'Sedentary',
        "color": 'red',
        "datapoints": ms,
    })

    datasequences.append({
        "title": 'LightlyActive',
        "color": 'orange',
        "datapoints": ml,
    })

    datasequences.append({
        "title": 'FairlyActive',
        "color": 'blue',
        "datapoints": mf,
    })

    datasequences.append({
        "title": 'VeryActive',
        "color": 'green',
        "datapoints": mv,
    })

    graph = {
        "graph": {
            'title': 'Activity Level (MINUTES)',
            'refreshEveryNSeconds': 600,
            'type': g_type,
            'datasequences': datasequences,
        }
    }

    return jsonify(graph)


# Filters
# ----------------------------

@app.template_filter()
def natural_time(datetime):
    """Filter used to convert Fitbit API's iso formatted text into
    an easy to read humanized format"""
    a = humanize.naturaltime(dateutil.parser.parse(datetime))
    return a


@app.template_filter()
def natural_number(number):
    """ Filter used to present integers cleanly """
    a = humanize.intcomma(number)
    return a


# Building Blocks
# ----------------------------

def get_creds(user_id):
    """Function takes user_id in and returns user_id, user_key, user_secret from db"""
    creds = User.query.filter_by(user_id=user_id).first_or_404()
    return creds


def get_connector(user_id):
    """Function takes user_id and returns variable to connect to fitbit from db"""
    x = get_creds(user_id)
    # print x

    connector = fitbit.Fitbit(
        # consumer_key=MY_CONSUMER_KEY,
        # consumer_secret=MY_CONSUMER_SECRET,
        # 'bcf9bd384513460395989025a2ede86a',
        # 'fd650ddb21c542c0a3ee3483ddda5727',
        MY_CONSUMER_KEY,
        MY_CONSUMER_SECRET,
        resource_owner_key=x.user_key,
        resource_owner_secret=x.user_secret)
        # resource_owner_key='bbcd07550f22360679689f69656c6583',
        # resource_owner_secret='548b251de5cb42675a6471bc0fb68536')
        # resource_owner_key=x.user_key,
        # resource_owner_secret=x.user_secret)
    return connector


def get_device_info(user_id):
    """ Function used to return device info
        https://wiki.fitbit.com/display/API/API-Get-Devices """
    device_info = get_connector(user_id).get_devices()
    return device_info


def get_user_profile(user_id):
    """ Function to return user profile
        https://wiki.fitbit.com/display/API/API-Get-User-Info """
    user_profile = get_connector(user_id).user_profile_get()
    return user_profile


@app.route('/debug/<user_id>')
def dev_dump(user_id):
    """ print info about a user for debugging, only enabled when debug is True """
    if app.debug:
        app.logger.info('running in dev mode, debugging enabled')
        app.logger.info(user_id)
        user = get_user_profile(user_id)
        # devices = get_device_info(user_id)
        return user
        # return render_template('debug.html', devices=devices)
    else:
        print "Not running in dev mode, therefore redir to index"
        return render_template('intro.html')


def get_daily_goals(user_id):
    """ Function to return daily goals
    https://wiki.fitbit.com/display/API/API-Get-Activity-Daily-Goals
    Not yet implemented
    """
    # user_goals = get_connector(user_id).get_activity_goals()
    pass


def output_json(dp, resource, datasequence_color, graph_type):
    """ Return a properly formatted JSON file for Statusboard """
    graph_title = ''
    datapoints = []
    for x in dp:
        datapoints.append(
            {'title': x['dateTime'], 'value': float(x['value'])})
    datasequences = []
    datasequences.append({
        "title": resource,
        # "color":        datasequence_color,
        "datapoints": datapoints,
    })

    graph = dict(graph={
        'title': graph_title,
        'yAxis': {'hide': False},
        'xAxis': {'hide': False},
        'refreshEveryNSeconds': 600,
        'type': graph_type,
        'datasequences': datasequences,
    })

    return graph
