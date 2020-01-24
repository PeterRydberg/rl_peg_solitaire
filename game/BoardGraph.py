import networkx as nx
import matplotlib.pyplot as plt
import itertools


class BoardGraph:
    def __init__(self, board_content, live_update_frequency):
        self.graph = nx.Graph()
        self.generate_graph(board_content)

        self.live_update_frequency = live_update_frequency

    def generate_graph(self, pegholes):
        edges = self.generate_networkx_edges(pegholes)
        self.graph.add_edges_from(edges)  # Add to visual graph
        self.init_graph()  # Draws the initial graph

    def init_graph(self):
        plt.ion()
        plt.axis('off')

    def show_graph(self):
        self.draw_graph()
        plt.show()
        plt.pause(self.live_update_frequency)

    def live_update_graph(self):
        plt.clf()
        self.draw_graph()
        plt.pause(self.live_update_frequency)

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(
            self.graph,
            pos=pos,
            node_color=self.get_color_list(self.graph.nodes),
            with_labels=False,
            font_weight='bold',
        )

    def get_color_list(self, nodes):
        colors = []
        for node in nodes:
            colors.append(self.get_node_color(node))

        return colors

    def get_node_color(self, node):
        if(node.content == 'filled'):
            return '#000000'
        elif(node.content == 'empty'):
            return '#ffffff'
        elif(node.content == 'selected'):
            return '#00ff00'
        elif(node.content == 'jump'):
            return 'ff0000'

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
