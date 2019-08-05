from flask import Flask, render_template #this has changed
from network_graph import create_plot, createNetworkGraph

app = Flask(__name__)

@app.route('/')
def index():

    bar = createNetworkGraph()
    return render_template('index.html', plot=bar)

if __name__ == '__main__':
    app.run()