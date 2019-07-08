CLIENT_ID = "0f7ac5c75709e1eb1558"
CLIENT_SECRET = "6be38a7698c54227cb8d27922ac222115916cbc7"
REDIRECT_URI = "http://localhost:65010/callback"

from uuid import uuid4
from flask import Flask,  abort, request
import requests
import requests.auth
import urllib.parse

state = str(uuid4())

app = Flask(__name__)
@app.route('/')
def homepage():
	text = '<a href="%s">Authenticate with Github</a>'
	return text % make_authorization_url()

@app.route('/callback')
def reddit_callback():
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = request.args.get('state', '')
	if not is_valid_state(state):
		# Uh-oh, this request wasn't started by us!
		abort(403)
	code = request.args.get('code')
	# We'll change this next line in just a moment
	return "got a code! %s" % get_user_emails(get_token(code))

def get_token(code):
    save_created_state(state)
    print("here")
    params = {"client_id": CLIENT_ID,
              "redirect_uri": REDIRECT_URI,
              "client_secret": CLIENT_SECRET,
              "code": code,
			  "state": state
			  }
    import urllib
    url = "https://github.com/login/oauth/access_token?" + urllib.parse.urlencode(params)
    response = requests.post(url)
    token = parse_response_text(response)
    return  token 

def parse_response_text(response):
    output = response.text.split("&")
    token = output[0].split("=")
    return token[1]

def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	save_created_state(state)
	params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "temporary",
			  "scope": "identity"}
	import urllib
	url = "https://github.com/login/oauth/authorize?" + urllib.parse.urlencode(params) 
	print(url)
	return url
    
def get_users(access_token):
	params = {"access_token": access_token}
	import urllib
	url = "https://api.github.com/user?" + urllib.parse.urlencode(params) 
	response = requests.get(url)
	return response.json()

def get_user_emails(access_token):
	json_response = get_users(access_token)
	email = json_response['email']
	return email
	    
    

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True


if __name__ == '__main__':
	app.run(debug=True, port=65010)