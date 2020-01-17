import networkx as nx
import matplotlib.pyplot as plt
import itertools


class BoardGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def generate_graph(self, pegholes):
        edges = []

        # Flattens list and accesses each pegholes' neighbors
        for peghole in list(itertools.chain(*pegholes)):
            for neighbor in peghole.neighbors:
                edges.append((peghole, neighbor))

        # Add to visual graph
        self.graph.add_edges_from(edges)

    def display_graph(self):
        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()

    # TODO: Render graph at a fixed angle
    # TODO: Render nodes with different colors depending on attributes
    # TODO: Make the graph render live as game goes on
