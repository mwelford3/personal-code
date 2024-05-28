import dash
from dash import dcc, html, Input, Output
import networkx as nx
import plotly.graph_objects as go
import pandas as pd

from_nodes = [1,2,3,4,1,2,1]
to_nodes =  [2,1,3,2,1,2,1]
data = pd.DataFrame({'from':from_nodes, 'to':to_nodes})
print(data)

G = nx.MultiDiGraph()

G.nodes(set(from_nodes))
for x,y in zip(data['from'], data['to']):
    G.add_edge(x,y)

print(G.edges)

nx.draw(G, with_labels=True, node_size=1000, node_color='r', edge_color='g', arrowsize=25)
