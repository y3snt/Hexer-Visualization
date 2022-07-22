from queue import PriorityQueue
from math import inf
from collections import namedtuple

# visualization purposes
Node = namedtuple('Node', 'num, prev_num, collected_swords') 
Edge = namedtuple('Edge', 'node, prev_node, weight, monsters')
Step = namedtuple('Step', 'edge, distance, state')

nodes = set() # needed for graph initialization
edges = set() # needed for graph initialization
steps = [] # animation is based on steps

def initialize(data):
    global n, m, p, k, K, G
    n, m, p, k, K, G = data

    reset_algorithm_values()

def reset_algorithm_values():
    global processed, dist, q

    processed = [ [False for j in range(1 << (p + 1))] for i in range(n + 1)] # true if i-th node with k-th state (subset of swords) was processed
    dist = [ [inf for j in range(1 << (p + 1))] for i in range(n + 1)] # distance to every town for every subset of swords (from town 1)
    q = PriorityQueue() # (distance, edge); (edge is used for visualization purposes)

def reset_visualization_values():
    global nodes, edges, steps

    nodes = set() 
    edges = set()
    steps = []

def win(mask, cost):
    '''Determine if we can cross the road to the next town.'''
    if cost == 0: return True
    for i in range(1, p + 1):
        if cost & (1 << i) and not (mask & (1 << i)): # if there is a monster on the road that we cannot defeat
            return False
    
    return True


def algorithm(): 
    bit_mask = K[1] # currently collected swords
    dist[1][bit_mask] = 0 # distance to current town with currently collected swords
    start_node = Node(1, 1, bit_mask)
    q.put((0, Edge(start_node, start_node, 0, 0)))

    nodes.add(start_node)

    # Dijkstra
    while not q.empty():
        d, current_edge = q.get()
        current_node = current_edge.node
        v, current_mask = current_node.num, current_node.collected_swords

        if processed[v][current_mask]: continue

        processed[v][current_mask] = True
        steps.append(Step(current_edge, d, 1)) # processing

        if v == n:
            print(f'Found!\nThe shortest distance to node {v} is {d}.')
            break

        for edge in G[v]:
            u, w, monsters = edge # next node, weight, monsters
            
            if win(current_mask, monsters):
                next_dist = dist[v][current_mask] + w
                next_mask = current_mask | K[u] # after collecting swords in the next town

                if  next_dist < dist[u][next_mask]:
                    next_node = Node(u, v, next_mask)
                    next_edge = Edge(next_node, current_node, w, monsters)
                    nodes.add(next_node)
                    edges.add(next_edge)
                    steps.append(Step(next_edge, next_dist, 2)) # to be processed

                    dist[u][next_mask] = next_dist
                    q.put((next_dist, next_edge))
        
        steps.append(Step(current_edge, d, 3)) # processed

def step():
    '''Return next step of the algorithm.'''
    for s in steps:
        yield s
