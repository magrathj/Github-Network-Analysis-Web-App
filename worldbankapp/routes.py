from worldbankapp import app

import json, plotly
from flask import render_template, request, Response, jsonify
from scripts.data import return_figures


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
	return render_template('index.html')