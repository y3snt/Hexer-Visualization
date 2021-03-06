import json

from visualization import Graph
from visualization import GraphAnimation
from algorithms.algorithm_visualization import algorithm, initialize, processing_node, to_be_processed_node, processed_node, new_edge, new_node
from data import Data

def add_node(node):
    nodes.add(node)

def add_edge(edge):
    edges.add(edge)

if __name__ == '__main__':
    # loading colors data
    with open('config/colors.json') as f:
        colors_data = json.load(f)
        node_colors, edge_colors, labels_colors = colors_data.values()
        node_colors, edge_colors = tuple(node_colors.values()), tuple(edge_colors.values())

    # loading sizes data
    with open('config/sizes.json') as f:
        sizes_data = json.load(f)
        node_sizes, edge_sizes, labels_sizes, border_sizes = sizes_data.values()
        node_sizes, edge_sizes, border_sizes = tuple(node_sizes.values()), tuple(edge_sizes.values()), tuple(border_sizes.values())

    # loading config data
    with open('config/config.json') as f:
        config = json.load(f)

    # initialization
    data = Data()
    with open('data/input.txt') as f:
        data.read_data(f)

    initialize(data)
    nodes = set() # needed for graph initialization
    edges = set() # needed for graph initialization
    graph = Graph(nodes, edges, config['seed'], 
        node_sizes, edge_sizes, labels_sizes, border_sizes, 
        node_colors, edge_colors, labels_colors)

    animation = GraphAnimation(graph, [processing_node, to_be_processed_node, processed_node])

    new_node += add_node
    new_edge += add_edge
    algorithm()

    graph.add_nodes(nodes)
    graph.add_edges(edges)
    
    print('nodes:', nodes)
    # animation
    animation.visualize(config['fps'], config['animation interval'], config['close seconds'], data.K, data.p)



# init empty graph(without nodes and edges), add event listeners -> run algorithm -> create nodes and edges -> add to graph -> animation