import networkx

import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json
from operator import itemgetter

import matplotlib.pyplot as plt
import networkx as nx

import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def createEgoGraph():
    # Create a BA model graph
    n = 1000
    m = 2
    G = nx.generators.barabasi_albert_graph(n, m)
    # find node with largest degree
    node_and_degree = G.degree()
    (largest_hub, degree) = sorted(node_and_degree, key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego = nx.ego_graph(G, largest_hub)
    # Draw graph
    pos = nx.spring_layout(hub_ego)
    nx.draw(hub_ego, pos, node_color='b', node_size=50, with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[largest_hub], node_size=300, node_color='r')
    plt.show()

def create_plot():


    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe


    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


def createNetworkGraph(json_dict, repo_owner):
    labels = []
    labels.append(repo_owner)

    for json_object in json_dict:
        labels.append(json_object['name'])

    G=nx.Graph()
    num_nodes = len(json_dict) + 1
    my_nodes=range(num_nodes)
    G.add_nodes_from(my_nodes)

    color_map = []
    color_map.append('black')
    for i in range(1, num_nodes):    
        G.add_edge(0, i)
        color_map.append('blue')

    pos=nx.spring_layout(G)   

    Xn=[pos[k][0] for k in range(len(pos))]
    Yn=[pos[k][1] for k in range(len(pos))]


    trace_nodes=dict(type='scatter',
                    x=Xn, 
                    y=Yn,
                    mode='markers',
                    marker=dict(size=40, color=color_map),
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
    layout=dict(title= '<br>Graph Network Repo',  
                font= dict(family='Balto'),
                width=1000,
                height=1000,
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




def createD3NetworkGraph():
    g = nx.karate_club_graph()
    fig, ax = plt.subplots(1, 1, figsize=(8, 6));
    nx.draw_networkx(g, ax=ax)
    nodes = [{'name': str(i), 'club': g.node[i]['club']}
         for i in g.nodes()]
    links = [{'source': u[0], 'target': u[1]}
            for u in g.edges()]
    graphJSON = json.dumps({'nodes': nodes, 'links': links}, indent=4,)
    return(graphJSON)
    #with open('graph.json', 'w') as f:
    #    json.dump({'nodes': nodes, 'links': links},
    #          f, indent=4,)


#if __name__ == '__main__':
#    createEgoGraph()