import networkx

import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json




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


