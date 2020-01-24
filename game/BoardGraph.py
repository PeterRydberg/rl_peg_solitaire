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

    def display_graph(self):
        pos = nx.spring_layout(self.graph)
        plt.ion()
        nx.draw(
            self.graph,
            pos=pos,
            node_color=self.get_color_list(self.graph.nodes),
            with_labels=False,
            font_weight='bold',
        )

        plt.axis('off')
        plt.show()
        self.live_update_graph()

    def live_update_graph(self):
        plt.pause(self.live_update_frequency)
        plt.clf()

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
