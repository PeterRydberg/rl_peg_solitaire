import networkx as nx
import matplotlib.pyplot as plt
import itertools


class BoardGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def generate_graph(self, pegholes):
        edges = self.generate_networkx_edges(pegholes)
        # Add to visual graph
        self.graph.add_edges_from(edges)

    def display_graph(self, pegholes):
        # edges = self.generate_networkx_edges
        flattened = list(itertools.chain(*pegholes))

        filled_nodes = list(filter(lambda x: x.content == 'filled', flattened))
        empty_nodes = list(filter(lambda x: x.content == 'empty', flattened))

        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(
            self.graph,
            pos=pos,
            nodelist=filled_nodes,
            node_color='#000000',
            with_labels=True,
            font_weight='bold'
        )
        nx.draw_networkx_nodes(
            self.graph,
            pos=pos,
            nodelist=empty_nodes,
            node_color='#ffffff',
            with_labels=True,
            font_weight='bold'
        )
        nx.draw_networkx_edges(
            self.graph,
            pos=pos,

        )
        plt.axis('off')
        plt.show()

    def generate_networkx_edges(self, pegholes):
        edges = []

        # Flattens list and accesses each pegholes' neighbors
        for peghole in list(itertools.chain(*pegholes)):
            for neighbor in peghole.neighbors:
                edges.append((peghole, neighbor))

        return edges

    # TODO: Render graph at a fixed angle
    # TODO: Render nodes with different colors depending on attributes
    # TODO: Make the graph render live as game goes on
