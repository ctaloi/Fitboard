import fitbit
from flask import render_template, flash, redirect, session, url_for, request, jsonify, send_from_directory
from app import app, db, mail, Message
from models import User
from random import choice
from flask_oauth import OAuth
import os

my_consumer_key = os.environ.get('CONSUMER_KEY')
my_consumer_secret = os.environ.get('CONSUMER_SECRET')

oauth = OAuth()
fitbit_app = oauth.remote_app(
    'fitbit',
    base_url='https://api.fitbit.com',
    request_token_url='http://api.fitbit.com/oauth/request_token',
    access_token_url='http://api.fitbit.com/oauth/access_token',
    authorize_url='http://www.fitbit.com/oauth/authorize',
    consumer_key=my_consumer_key,
    consumer_secret=my_consumer_secret
)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


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
    msg.body = "NOTICE %s \n Logile Attached \n" % (message)
    mail.send(msg)
    return


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


@app.route('/graph/<act>')
def build_charts(act):

    user = session['fitbit_keys'][0]
    data = get_activity(user, act, '3m', 'raw')
    act = []
    for item in data:
        act.append([str(item['dateTime']), float(item['value'])])
    return render_template('view_charts.html', data=act)


@fitbit_app.tokengetter
def get_fitbit_app_token(token=None):
    return session.get('fitbit_app_token')


@app.route('/login')
def login():
    email_alert('NEW LOGIN')
    return fitbit_app.authorize(
        callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))


@app.route('/oauth_authorized')
@fitbit_app.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('charts')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

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
    """Drop user from databaase"""
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
    session.pop('fitbit_keys', None)
    session.pop('user_profile', None)
    return redirect(url_for('index'))


def get_creds(user_id):
    """Function takes user_id in and returns user_id, user_key, user_secret from db"""
    creds = User.query.filter_by(user_id=user_id).first_or_404()
    return creds


def get_connector(user_id):
    """Function takes user_id and returns variable to connect to fitbit from db"""
    x = get_creds(user_id)

    connector = fitbit.Fitbit(
        consumer_key=my_consumer_key,
        consumer_secret=my_consumer_secret,
        user_key=x.user_key,
        user_secret=x.user_secret)
    return connector


def get_device_info(user_id):
    device_info = get_connector(user_id).get_devices()
    return device_info


def get_user_profile(user_id):
    user_profile = get_connector(user_id).user_profile_get()
    return user_profile


@app.route('/u/<user_id>/<resource>/<period>')
def get_activity(user_id, resource, period='1w', return_as='json'):
    app.logger.info('resource, %s, %s, %s, %s, %s' % (
        user_id, resource, period, return_as, request.remote_addr))
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

    the_data = get_connector(user_id).time_series(
        slash_resource, base_date='today', period=period)[dash_resource]

    if return_as == 'raw':
        return the_data
    if return_as == 'json':
        return jsonify(output_json(the_data, resource, datasequence_color, graph_type))


@app.route('/u/summary/<user_id>/<period>')
def get_levelsummary(user_id, period):

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
        ms.append({'title':  x['dateTime'], 'value': float(x['value']) - 480})
    for x in minutesLightlyActive:
        ml.append({'title':  x['dateTime'], 'value': float(x['value'])})
    for x in minutesFairlyActive:
        mf.append({'title':  x['dateTime'], 'value': float(x['value'])})
    for x in minutesVeryActive:
        mv.append({'title':  x['dateTime'], 'value': float(x['value'])})

    datasequences.append({
        "title":        'Sedentary',
        "color":        'red',
        "datapoints":   ms,
    })

    datasequences.append({
        "title":        'LightlyActive',
        "color":        'orange',
        "datapoints":   ml,
    })

    datasequences.append({
        "title":        'FairlyActive',
        "color":        'blue',
        "datapoints":   mf,
    })

    datasequences.append({
        "title":        'VeryActive',
        "color":        'green',
        "datapoints":   mv,
    })

    graph = {
        "graph":    {
            'title':                'Activity Level (MINUTES)',
            'refreshEveryNSeconds':  240,
            'type':                 g_type,
            'datasequences':        datasequences,
        }
    }

    return jsonify(graph)


def output_json(dp, resource, datasequence_color, graph_type):
    ''' Outputs a json object for a statusboard graph '''

    graph_title = ''
    datapoints = []
    for x in dp:
        datapoints.append({'title':  x[
                          'dateTime'], 'value': float(x['value'])})
    datasequences = []
    datasequences.append({
        "title":        resource,
        # "color":        datasequence_color,
        "datapoints":   datapoints,
    })

    graph = {
        "graph":    {
            'title':                graph_title,
            'yAxis':                {'hide': False},
            'xAxis':                {'hide': False},
            'refreshEveryNSeconds': 240,
            'type':                 graph_type,
            'datasequences':        datasequences,
        }
    }

    return graph
