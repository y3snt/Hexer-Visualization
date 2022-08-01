import json
from copy import deepcopy

from visualization import Graph
from visualization import GraphAnimation
from algorithms.algorithm_visualization import Algorithm
from data import Data
from utils.bitmasks import bit_mask_to_list

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

    algorithm = Algorithm(*deepcopy(data))
    nodes = set() # needed for graph initialization (all nodes that will appear during the animation)
    edges = set() # needed for graph initialization (all edges that will appear during the animation)
    graph = Graph(nodes, edges, config['seed'], 
        node_sizes, edge_sizes, labels_sizes, border_sizes, 
        node_colors, edge_colors, labels_colors)

    animation = GraphAnimation(graph, algorithm.events[:3])

    # events subscription
    algorithm.new_node += add_node
    algorithm.new_edge += add_edge

    algorithm.run()

    graph.add_nodes(nodes)
    graph.add_edges(edges)
    
    # animation
    animation.visualize(
        config['fps'], config['animation interval'], config['close seconds'],
        lambda node_num: bit_mask_to_list(data.K[node_num], data.p),
        lambda mask: bit_mask_to_list(mask, data.p),
        lambda mask: bit_mask_to_list(mask, data.p)
    )