import matplotlib.animation as animation
import matplotlib.pyplot as plt
from threading import Timer
from collections import namedtuple
from enum import Enum

class State(Enum):
    '''Edges states.'''

    PROCESSING = 1
    TO_BE_PROCESSED = 2
    PROCESSED = 3

Step = namedtuple('Step', 'edge, distance, state')

class GraphAnimation:
    def __init__(self, graph, step_events: list):
        self.graph = graph
        self._steps = [] # animation steps

        # subscribing events
        self._step_funcs = [self._step_func(state) for state in State] # functions, with assigned state, that add step to _steps 
        for i, event in enumerate(step_events):
            event += self._step_funcs[i] # function corresponding to the event

    def visualize(self, fps, interval, close_seconds, second_label_func=lambda x: x, upper_label_func=lambda x: x, edge_sub_label_func=lambda x: x):
        step_gen = self._step()
        def _animate(i):
            self.fig.clear()
            self.graph.draw()
            try:
                current_edge, current_dist, state = next(step_gen)
            except StopIteration:
                anim.event_source.stop()
                t = Timer(close_seconds, plt.close, args=None, kwargs=None)
                t.start()
            else:
                current_node = current_edge.node
                self.graph.update_node(current_node, second_label_func(current_node.num), upper_label_func(current_node.collected_swords), current_dist, state.value)
                self.graph.update_edge(current_edge, edge_sub_label_func(current_edge.monsters), state.value)

        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        self.fig = plt.gcf()
        anim = animation.FuncAnimation(self.fig, _animate, frames=fps, interval=interval, repeat=False)
        plt.show()

    def _step(self):
        '''Return next step of the algorithm.'''
        for s in self._steps:
            yield s

    def _step_func(self, state):
        '''Return function, which adds steps with a given state.'''
        def add_step(edge, distance):
            self._steps.append(Step(edge, distance, state)) 
            
        return add_step