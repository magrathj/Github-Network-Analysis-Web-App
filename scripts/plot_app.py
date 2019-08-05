from flask import Flask, render_template #this has changed
from network_graph import create_plot, createNetworkGraph
import json
import urllib
import requests
import requests.auth

app = Flask(__name__)


#with open('repos.json', 'r') as f:
#    distros_dict = json.load(f)


url = "https://api.github.com/users/magrathj/repos"
response = requests.get(url)
distros_dict = json.loads(response.text)



@app.route('/')
def index():
    bar = createNetworkGraph(distros_dict, 'magrathj')
    return render_template('index.html', plot=bar)

if __name__ == '__main__':
    app.run()