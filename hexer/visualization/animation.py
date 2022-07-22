import matplotlib.animation as animation
import matplotlib.pyplot as plt
from threading import Timer

from utils.bitmasks import bit_mask_to_list

class GraphAnimation:
    def __init__(self, graph):
        self.graph = graph

    def visualize(self, fps, interval, close_seconds, steps, K, p):
        def _animate(i):
            self.fig.clear()
            self.graph.draw_graph()
            try:
                current_edge, current_dist, state = next(steps)
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
