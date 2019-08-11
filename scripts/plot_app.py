from flask import Flask, render_template #this has changed
from network_graph import create_plot, createNetworkGraph,  createD3NetworkGraph, createD3NetworkGraphSecond
import json
import urllib
import requests
import requests.auth

app = Flask(__name__)


def get_users_repos_json_response(url):    
    response = requests.get(url)
    distros_dict = json.loads(response.text)
    return(distros_dict)


#@app.route('/')
#def index():
#    distros_dict = get_users_repos_json_response(url = "https://api.github.com/users/magrathj/repos")
#    bar = createNetworkGraph(distros_dict, 'magrathj')
#    return render_template('plot.html', plot=bar)

@app.route('/')
def index():
    #return render_template('d3.html')
    chart_data = createD3NetworkGraph()
    data = {'chart_data': chart_data}
    return render_template("d3.html", data=data)


if __name__ == '__main__':
    app.run()