from dataclasses import dataclass, field
from typing import List, Tuple
from queue import PriorityQueue
from math import inf
from collections import namedtuple

from events import Event

# visualization purposes
Node = namedtuple('Node', 'num, prev_num, collected_swords') 
Edge = namedtuple('Edge', 'node, prev_node, weight, monsters') 

@dataclass
class Algorithm():
    # data values
    n: int # number of towns (number of nodes)  
    m: int # number of roads connecting the towns (number of edges) 
    p: int # number of different kinds of monsters 
    k: int # number of blacksmiths 

    K: List[int] = field(default_factory=list) # list of bit masks, that represents swords that can be obtained in every town
    G: List[List[Tuple[int, int, int]]] = field(default_factory=list) # weighted graph that represents towns and monsters on the roads

    # algorithm values
    processed: List[List[bool]] = field(init=False, default_factory=list) # true if i-th node with k-th state (subset of swords) was processed
    dist: List[List[int]] = field(init=False, default_factory=list) # distance to every town for every subset of swords (from town 1)
    q: PriorityQueue = field(init=False, default_factory=PriorityQueue) # (distance, edge); (edge is used for visualization purposes)

    # events
    processing_node: Event = field(init=False, default_factory=Event)
    to_be_processed_node: Event = field(init=False, default_factory=Event)
    processed_node: Event = field(init=False, default_factory=Event)

    new_node: Event = field(init=False, default_factory=Event)
    new_edge: Event = field(init=False, default_factory=Event)

    events: List[Event] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.events = [self.processing_node, self.to_be_processed_node, self.processed_node, self.new_node, self.new_edge]
        self.reset_algorithm_values()

    def reset_algorithm_values(self) -> None:
        '''Reset initial values, so algorithm can be called again (with the same data).'''
        self.processed = [ [False for j in range(1 << (self.p + 1))] for i in range(self.n + 1)] 
        self.dist = [ [inf for j in range(1 << (self.p + 1))] for i in range(self.n + 1)] 
        self.q = PriorityQueue() 

    def _win(self, collected_swords: int, monsters: int) -> bool:
        '''Determine if we can cross the road to the next town.
        
        Args:
            collected_swords: Bit mask representing types of currently collected swords
            monsters: Bit mask representing types of monsters on the road that we're trying to cross
        
        Returns:
            True if the road can be crossed, otherwise False.

        '''
        if monsters == 0: return True
        for i in range(1, self.p + 1):
            if monsters & (1 << i) and not (collected_swords & (1 << i)): # if there is a monster on the road that we cannot defeat
                return False
        
        return True

    def run(self) -> None: 
        '''Run the algorithm.'''
        bit_mask = self.K[1] # currently collected swords
        self.dist[1][bit_mask] = 0 # distance to current town with currently collected swords
        start_node = Node(1, 1, bit_mask)
        self.q.put((0, Edge(start_node, start_node, 0, 0)))

        self.new_node(start_node)

        # Dijkstra
        while not self.q.empty():
            current_dist, current_edge = self.q.get()
            current_node = current_edge.node
            current_node_num, current_mask = current_node.num, current_node.collected_swords

            if self.processed[current_node_num][current_mask]: continue

            self.processed[current_node_num][current_mask] = True
            self.processing_node(current_edge, current_dist)

            if current_node_num == self.n:
                print(f'Found!\nThe shortest distance to node {current_node_num} is {current_dist}.')
                break

            for edge in self.G[current_node_num]:
                next_node_num, weight, monsters = edge
                
                if self._win(current_mask, monsters):
                    next_dist = self.dist[current_node_num][current_mask] + weight
                    next_mask = current_mask | self.K[next_node_num] # after collecting swords in the next town

                    if  next_dist < self.dist[next_node_num][next_mask]:
                        next_node = Node(next_node_num, current_node_num, next_mask)
                        next_edge = Edge(next_node, current_node, weight, monsters)
                        self.new_node(next_node)
                        self.new_edge(next_edge)
                        self.to_be_processed_node(next_edge, next_dist)

                        self.dist[next_node_num][next_mask] = next_dist
                        self.q.put((next_dist, next_edge))
            
            self.processed_node(current_edge, current_dist)
