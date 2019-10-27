CLIENT_ID = "0f7ac5c75709e1eb1558"
CLIENT_SECRET = "6be38a7698c54227cb8d27922ac222115916cbc7"
REDIRECT_URI = "http://localhost:65010/callback"

from uuid import uuid4
from flask import Flask,  abort, request
import requests
import requests.auth
import urllib.parse
from flask import redirect
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['github_db']

coll_user = db['users']
coll_repos = db['repos']
coll_followers = db['followers']
coll_followering = db['followering']


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
	access_token = get_token(code)
	get_initial_user = get_users(access_token)

	following_urls = get_following(get_initial_user)
	followers_urls = get_followers(get_initial_user)

	recursive_get_user_data(following_urls=following_urls, followers_urls=followers_urls, access_token=access_token)

	return("hey")
	#return get_following(get_users(get_token(code))).text #get_repos(get_users(get_token(code))).text #redirect(get_user_webpage(get_users(get_token(code))), code=302) # "got a code! %s" % get_users(get_token(code))
	



def recursive_get_user_data(following_urls, followers_urls, access_token):
	for url in following_urls:
		print(get_new_users(url, access_token, coll_followering))
	
	for url in followers_urls:
		print(get_new_users(url, access_token, coll_followers))

	return()



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
	return url
    
def get_users(access_token):
	params = {"access_token": access_token}
	import urllib
	url = "https://api.github.com/user?" + urllib.parse.urlencode(params) 
	response = requests.get(url)
	
	# store user into user collection
	response_json = response.json()	
	x = coll_user.insert_one(response_json)

	# get users repos 
	repos = get_repos(response_json)

	# store user's repos into repos collections
	repos_json = repos.json()
	x = coll_repos.insert_many(repos_json)

	return response.json() 

def get_new_users(url, access_token, mycol):
	params = {"access_token": access_token}
	import urllib
	url = url + '?' + urllib.parse.urlencode(params) 
	response = requests.get(url)

	# store user into either following/follower collection
	response_json = response.json()	
	x = mycol.insert_one(response_json)

	# get users repos 
	repos = get_repos(response_json)

	# store user's repos into repos collections
	repos_json = repos.json()
	x = coll_repos.insert_many(repos_json)

	return response.json()

def get_user_webpage(json_response):
	html_url = json_response['html_url']
	return html_url


def get_user_emails(json_response):
	email = json_response['email']
	return email

def get_user_login_name(json_response):
	login = json_response['login']
	return login	    
    
def get_user_name(json_response):
	name = json_response['name']
	return name	    
    
def get_followers(json_response):
	url = json_response['followers_url']
	import urllib 
	response = requests.get(url).json()
	url = []
	for input in response:
		url.append(input['url'])
		print(input['url'])
	return url

def get_following(json_response):
	print(json_response)
	url = json_response['following_url']
	import urllib 
	url, _ = url.split('{')
	print(url)
	response = requests.get(url).json()
	url = []
	for input in response:
		print(input)
		url.append(input['url'])
		#print(input['url'])
	return url
  

def get_repos(json_response):
	url = json_response['repos_url']
	import urllib 
	response = requests.get(url)
	response_json = response.json()
	#x = coll_repos.insert_many(response_json)
	#print(x.inserted_ids)
	return response


def get_collaborators(json_repos, access_token):
	params = {"access_token": access_token}
	import urllib
	url = "https://api.github.com/repos/magrathj/shinyforms/collaborators" + urllib.parse.urlencode(params)
	return url

# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True

## TODO create class repo to hold individual repos
class Repo:
	def __init__(self, repo_name, repo_url):
		self.repo_name = repo_name
		self.repo_url = repo_url


## TODO create class user to hold individual user details
class User:
	def __init__(self, name, github_url, login):
		self.name = name
		self.github_url = github_url
		self.login = login


## TODO create class Github to handle all Github methods
class Github:
	def __init__(self, client_id, client_secret):
		self.client_id = client_id
		self.client_secret = client_secret




if __name__ == '__main__':
	app.run(debug=True, port=65010)