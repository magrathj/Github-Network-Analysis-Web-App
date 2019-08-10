from worldbankapp import app

import json, plotly
from flask import render_template, request, Response, jsonify,  Flask,  abort, redirect
from uuid import uuid4
import requests
import requests.auth
import urllib.parse
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot


CLIENT_ID = "0f7ac5c75709e1eb1558"
CLIENT_SECRET = "6be38a7698c54227cb8d27922ac222115916cbc7"
REDIRECT_URI = "https://github-network-app.herokuapp.com/callback"
#REDIRECT_URI = "http://127.0.0.1:5000/callback"

state = str(uuid4())


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
	return render_template('index.html')


@app.route("/forward/", methods=['POST'])
def move_forward():
    return redirect(make_authorization_url())


@app.route('/about/', methods=['POST', 'GET'])
def aboutpage():
    title = "Github Network App"
    paragraph = ["This app"]
    pageType = 'about'
    return render_template("about.html", title=title, paragraph=paragraph, pageType=pageType)

@app.route('/callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
    	return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
    	abort(403)
    code = request.args.get('code')    
    token = get_token(code)
    user = get_users(token)
    repo_url = get_repos(user)
    json_output = get_users_repos_json_response(repo_url) 
    bar = createNetworkGraph(json_output, get_user_login_name(user))
    print(get_collaborators(json_output, token))
    return render_template('plot.html', plot=bar)


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
	response = requests.get(url)
	return response.json()
   
def get_repos(json_response):
	url = json_response['repos_url']
	return url


def get_users_repos_json_response(url):    
    response = requests.get(url)
    distros_dict = json.loads(response.text)
    return(distros_dict)


def get_collaborators(json_response, access_token):
    print(access_token)
    for json_object in json_response:
        url = json_object['contributors_url']
        print(url)
        json_collaborator = get_list_of_collaborators(url)
        print(json_collaborator)
    return ''

def get_collaborator_url(collaborators_url, access_token):
	params = {"access_token": access_token}
	import urllib
	url = collaborators_url + urllib.parse.urlencode(params)
	return url

def get_list_of_collaborators(url):
    response = requests.get(url)
    distros_dict = json.loads(response.text)
    return distros_dict



def createNetworkGraph(json_dict, repo_owner):
    labels = []
    labels.append(repo_owner)

    for json_object in json_dict:
        labels.append(json_object['name'])

    G=nx.Graph()#  G is an empty Graph
    num_nodes = len(json_dict) + 1
    my_nodes=range(num_nodes)
    G.add_nodes_from(my_nodes)

    for i in range(1, len(json_dict) + 1):    
        G.add_edge(0, i)

    pos=nx.fruchterman_reingold_layout(G)   

    Xn=[pos[k][0] for k in range(len(pos))]
    Yn=[pos[k][1] for k in range(len(pos))]


    trace_nodes=dict(type='scatter',
                    x=Xn, 
                    y=Yn,
                    mode='markers',
                    marker=dict(size=28, color='rgb(0,240,0)'),
                    text=labels,
                    hoverinfo='text')

    Xe=[]
    Ye=[]
    for e in G.edges():
        Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
        Ye.extend([pos[e[0]][1], pos[e[1]][1], None])

    trace_edges=dict(type='scatter',
                    mode='lines',
                    x=Xe,
                    y=Ye,
                    line=dict(width=1, color='rgb(25,25,25)'),
                    hoverinfo='none' 
                    )

    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
            zeroline=False,
            showgrid=False,
            showticklabels=False,
            title='' 
            )
    layout=dict(title= 'My Graph',  
                font= dict(family='Balto'),
                width=600,
                height=600,
                autosize=False,
                showlegend=False,
                xaxis=axis,
                yaxis=axis,
                margin=dict(
                l=40,
                r=40,
                b=85,
                t=100,
                pad=0,
        
        ),
        hovermode='closest',
        plot_bgcolor='#efecea', #set background color            
        )


    fig = dict(data=[trace_edges, trace_nodes], layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return(graphJSON)


def save_created_state(state):
	pass
def is_valid_state(state):
	return True