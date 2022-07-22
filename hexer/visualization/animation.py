import matplotlib.animation as animation
import matplotlib.pyplot as plt
from threading import Timer
from collections import namedtuple

from utils.bitmasks import bit_mask_to_list

Node = namedtuple('Node', 'num, prev_num, collected_swords') 
Edge = namedtuple('Edge', 'node, prev_node, weight, monsters')
Step = namedtuple('Step', 'edge, distance, state')

class GraphAnimation:
    def __init__(self, graph, step_events: list): # + states enum, methods list len
        self.graph = graph
        self._steps = [] # animation steps
        for event in step_events:
            event += self._add_step

    def visualize(self, fps, interval, close_seconds, K, p):
        step_gen = self._step()
        def _animate(i):
            self.fig.clear()
            self.graph.draw_graph()
            try:
                current_edge, current_dist, state = next(step_gen)
            except StopIteration:
                anim.event_source.stop()
                t = Timer(close_seconds, plt.close, args=None, kwargs=None)
                t.start()
            else:
                current_node = current_edge.node
                self.graph.update_node(current_node, bit_mask_to_list(K[current_node.num], p), bit_mask_to_list(current_node.collected_swords, p), current_dist, state)
                self.graph.update_edge(current_edge, bit_mask_to_list(current_edge.monsters, p), state)

        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        self.fig = plt.gcf()
        anim = animation.FuncAnimation(self.fig, _animate, frames=fps, interval=interval, repeat=False)
        plt.show()

    def _add_step(self, edge, distance, state):
        self._steps.append(Step(edge, distance, state)) #TODO remove state

    def _step(self):
        '''Return next step of the algorithm.'''
        for s in self._steps:
            yield s

