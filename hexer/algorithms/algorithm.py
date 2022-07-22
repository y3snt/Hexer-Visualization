from queue import PriorityQueue
from math import inf

def initialize(data):
    global n, m, p, k, K, G
    n, m, p, k, K, G = data

    reset_algorithm_values()

def reset_algorithm_values():
    global processed, dist, q

    processed = [ [False for j in range(1 << (p + 1))] for i in range(n + 1)] # true if i-th node with k-th state (subset of swords) was processed
    dist = [ [inf for j in range(1 << (p + 1))] for i in range(n + 1)] # distance to every town (from town 1) for every subset of swords
    q = PriorityQueue() # (distance, node number, state)

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
    q.put((0, 1, bit_mask))

    # Dijkstra
    while not q.empty():
        d, v, current_mask = q.get()
        if processed[v][current_mask]: continue
        if v == n:
            return d

        processed[v][current_mask] = True

        for edge in G[v]:
            u, w, monsters = edge # next node, weight, monsters
            if win(current_mask, monsters):
                next_mask = current_mask | K[u] # after collecting swords in the next town
                if dist[v][current_mask] + w < dist[u][next_mask]:
                    dist[u][next_mask] = dist[v][current_mask] + w
                    q.put((dist[u][next_mask], u, next_mask))

    return -1

