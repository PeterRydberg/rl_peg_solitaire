import networkx as nx
import matplotlib.pyplot as plt
import itertools


class BoardGraph:
    def __init__(self, board_content, board_type, live_update_frequency):
        self.graph = nx.Graph()
        self.live_update_frequency = live_update_frequency

        self.generate_graph(board_content)
        self.pos = self.compute_positions(100, board_type)

    def generate_graph(self, pegholes):
        edges = self.generate_networkx_edges(pegholes)
        self.graph.add_edges_from(edges)  # Add to visual graph
        self.init_graph()  # Draws the initial graph

    def init_graph(self):
        plt.ion()
        plt.axis('off')

    def show_graph(self, episode_number):
        self.draw_graph(episode_number)
        plt.show()
        plt.pause(self.live_update_frequency)  # Used when only blocking GPU

    def live_update_graph(self):
        plt.clf()
        self.draw_graph()
        plt.pause(self.live_update_frequency)  # Used when only blocking GPU

    def draw_graph(self, episode_number):
        plt.clf()
        plt.title(f'Episode {episode_number}')
        nx.draw(
            self.graph,
            pos=self.pos,
            node_color=self.get_color_list(self.graph.nodes),
            with_labels=False,
            font_weight='bold',
        )

    def compute_positions(self, size, board_type):
        pos = {}
        step = size / 10

        for node in self.graph:
            (x, y) = node.coordinates

            # Generates specific board coordinates
            if(board_type == "triangle"):
                xpos = size + (-step) * (x/2) + step * y
                ypos = size + (-step) * x
            elif(board_type == "diamond"):
                xpos = size + (-step) * x + step * y
                ypos = size + (-step) * x + (-step) * y
            pos[node] = (xpos, ypos)

        return pos

    def get_color_list(self, nodes):
        colors = []
        for node in nodes:
            colors.append(self.get_node_color(node))

        return colors

    def get_node_color(self, node):
        if(node.content == 'filled'):
            return '#2b2b2b'
        elif(node.content == 'empty'):
            return '#c4c4c4'
        elif(node.content == 'selected'):
            return '#103f37'
        elif(node.content == 'jump'):
            return '#6b1c08'

    def generate_networkx_edges(self, pegholes):
        edges = []
        # Flattens list and accesses each pegholes' neighbors
        for peghole in list(itertools.chain(*pegholes)):
            for neighbor in peghole.neighbors:
                if(neighbor):
                    edges.append((peghole, neighbor))

        return edges

    # TODO: Render graph at a fixed angle
    # TODO: Render nodes with different colors depending on attributes
    # TODO: Make the graph render live as game goes on
