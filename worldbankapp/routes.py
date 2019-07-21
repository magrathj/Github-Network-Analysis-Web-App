from worldbankapp import app

import json, plotly
from flask import render_template, request, Response, jsonify,  Flask,  abort, redirect
from scripts.data import return_figures
from uuid import uuid4
import requests
import requests.auth
import urllib.parse

CLIENT_ID = "0f7ac5c75709e1eb1558"
CLIENT_SECRET = "6be38a7698c54227cb8d27922ac222115916cbc7"
REDIRECT_URI = "http://localhost:65010/callback"

state = str(uuid4())

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
	return render_template('index.html')


@app.route("/forward/", methods=['POST'])
def move_forward():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('index.html', message=forward_message);
