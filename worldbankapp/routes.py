from worldbankapp import app
import json, plotly
from flask import render_template, request, Response, jsonify
from scripts.data import return_figures

from flask import flask, redirect, request, session
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Waffling on is really great for these secrets brandy cactus beartrap'

@app.route('/callback')
def callback():
    if 'code' in request.args:
        url = 'https://github.com/login/oauth/access_token'
        payload = {
            'client_id': environ.get('CLIENT_ID'),
            'client_secret': environ.get('CLIENT_SECRET'),
            'code': request.args['code']
        }
        headers = {'Accept': 'application/json'}
        r = requests.post(url, params=payload, headers=headers)
        response = r.json()
        # get access_token from response and store in session
        if 'access_token' in response:
            session['access_token'] = response['access_token']
        else:
            app.logger.error('github didn\'t return an access token, oh dear')
        # send authenticated user where they're supposed to go
        return redirect(url_for('index'))
    return '', 404

@app.route('/')
def index():
    # authenticated?
    if not 'access_token' in session:
        return 'Never trust strangers', 404
    # get username from github api
    url = 'https://api.github.com/user?access_token={}'
    r = requests.get(url.format(session['access_token']))
    try:
        login = r.json()['login']
    except AttributeError:
        app.logger.debug('error getting username from github, whoops')
        return 'I dont know who you are; I should, but regretfully I dont', 500
    return 'Hello {}!'.format(login), 200


if __name__ == '__main__':
	app.run(debug=True, port=65010)