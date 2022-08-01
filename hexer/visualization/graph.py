import networkx as nx
from copy import deepcopy

class Graph:
    def __init__(
            self, nodes, edges, layout_seed, 
            node_sizes, edge_sizes, labels_sizes, border_sizes, 
            node_colors, edge_colors, labels_colors):
        
        self.node_labels = {} 
        self.edge_labels = {} 
        self.lower_node_labels = {} 
        self.upper_node_labels = {} 
        
        self.seed = layout_seed

        self.graph = nx.Graph()
        
        self.node_sizes, self.edge_sizes, self.labels_sizes, self.border_sizes = node_sizes, edge_sizes, labels_sizes, border_sizes
        self.node_colors, self.edge_colors, self.labels_colors =  node_colors, edge_colors, labels_colors

        self.add_nodes(nodes)
        self.add_edges(edges)

        self._update_graph()
        
    def add_nodes(self, nodes):
        if nodes:
            self.graph.add_nodes_from((u, v, mask) for u, v, mask in nodes)
            self._update_graph()

    def add_edges(self, edges):
        if edges:
            self.graph.add_edges_from((U, V) for U, V, t, b in edges)
            self._update_graph()

    def _update_graph(self):
        self.pos = nx.spring_layout(self.graph, seed=self.seed)

        # change node labels positions
        self.upper_node_labels_pos = deepcopy(self.pos)
        self.lower_node_labels_pos = deepcopy(self.pos)

        for i in self.upper_node_labels_pos:
            self.upper_node_labels_pos[i][1] += 0.039
            self.lower_node_labels_pos[i][1] -= 0.037
            
        self._init_node_attributes()
        self._init_edge_attributes()

    def draw(self):
        nx.draw(self.graph, self.pos, node_color=list(nx.get_node_attributes(self.graph, 'color').values()), edge_color=self.edge_colors[0])
        nx.draw_networkx_nodes(self.graph, self.pos, linewidths=list(nx.get_node_attributes(self.graph, 'border size').values()), edgecolors=self.node_colors[2], node_size=list(nx.get_node_attributes(self.graph, 'size').values()), node_color=list(nx.get_node_attributes(self.graph, 'color').values()))
        nx.draw_networkx_edges(self.graph, self.pos, style=list(nx.get_edge_attributes(self.graph, 'style').values()), width=self.edge_sizes[0], edge_color=list(nx.get_edge_attributes(self.graph, 'color').values()))
        nx.draw_networkx_edge_labels(self.graph, self.pos, self.edge_labels, font_size=self.labels_sizes['edge label'])
        nx.draw_networkx_labels(self.graph, self.pos, labels=self.node_labels, font_color=self.labels_colors['node label'], font_size=self.labels_sizes['node label'])
        nx.draw_networkx_labels(self.graph, self.lower_node_labels_pos, labels=self.lower_node_labels, font_color=self.labels_colors['lower node label'], font_size=self.labels_sizes['lower node label'])
        nx.draw_networkx_labels(self.graph, self.upper_node_labels_pos, labels=self.upper_node_labels, font_color=self.labels_colors['upper node label'], font_size=self.labels_sizes['upper node label'])


    def update_node(self, node, second_label, upper_label, dist, state):
        self._update_node_attributes(node, state)
        self._update_node_label(node, second_label)
        self._update_lower_node_label(node, dist)
        if state == 1: self._update_upper_node_label(node, upper_label)
                   
    def update_edge(self, edge, sub_label, state):
        self._update_edge_attributes(edge, state)
        self._update_edge_label(edge, sub_label)

    def _init_node_attributes(self):
        nx.set_node_attributes(self.graph, self.node_sizes[0], 'size')
        nx.set_node_attributes(self.graph, self.border_sizes[0], 'border size')
        nx.set_node_attributes(self.graph, self.node_colors[0], 'color')

    def _update_node_attributes(self, node, state):
        nx.set_node_attributes(self.graph, {node: self.node_colors[state]}, name='color')
        nx.set_node_attributes(self.graph, {node: self.node_sizes[state]}, name='size')
        nx.set_node_attributes(self.graph, {node: self.border_sizes[state]}, name='border size')

    def _update_edge_attributes(self, edge, state):
        nx.set_edge_attributes(self.graph, {(edge.node, edge.prev_node): self.edge_colors[state]}, name='color')
        if state == 2: nx.set_edge_attributes(self.graph, {(edge.node, edge.prev_node): 'dashed'}, name='style')
        else: nx.set_edge_attributes(self.graph, {(edge.node, edge.prev_node): 'solid'}, name='style')

    def _init_edge_attributes(self):
        nx.set_edge_attributes(self.graph, self.edge_colors[0], 'color')
        nx.set_edge_attributes(self.graph, 'solid', 'style')

    def _update_node_label(self, node, second_label):
        self.node_labels[node] = f'{node.num}\n{second_label}' if second_label else f'{node.num}'

    def _update_edge_label(self, edge, second_label):
        U, V, w, b = edge
        self.edge_labels[(U, V)] = f'{w}\n{second_label}' if second_label else f'{w}'

    def _update_upper_node_label(self, node, label):
        self.upper_node_labels[node] = f'{label}' if label else ''

   
    def _update_lower_node_label(self, node, label):    
        self.lower_node_labels[node] = label
    