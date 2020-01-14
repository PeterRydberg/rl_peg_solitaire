from Peghole import Peghole

import math

import networkx as nx
import matplotlib.pyplot as plt


class Board:
    def __init__(self, board_type, height, initial_empty={}):
        self.board_type = board_type
        self.height = height

        # If empty holes are unspecified
        if(not initial_empty):
            initial_empty = {
                (math.floor(self.height / 2), math.floor(self.height / 2))
                }
        self.contents = []
        self.generate_board(initial_empty)

    def generate_board(self, initial_empty):
        if(self.board_type == 'triangle'):
            self.gen_triangle_board(initial_empty)
        elif(self.board_type == 'diamond'):
            self.gen_diamond_board(initial_empty)
        else:
            print("Not a valid board shape")

    # Board generation for triangular boards
    def gen_triangle_board(self, initial_empty):
        graph_list_representation = []

        for x in range(self.height):
            graph_list_representation.append(
                    [Peghole('filled') for _ in range(x + 1)]
                )

        # Removes peg contents for each coordinate of initial holes
        for empty_peg in initial_empty:
            xpos = empty_peg[0]
            ypos = empty_peg[1]
            graph_list_representation[xpos][ypos].content = 'empty'

        self.contents = graph_list_representation
        graph = nx.Graph()

        for r, row in enumerate(graph_list_representation):
            for c, item in enumerate(row):
                edge_indexes = [
                    (r-1, c),
                    (r, c+1),
                    (r+1, c+1),
                    (r+1, c),
                    (r, c-1),
                    (r-1, c-1)
                ]

                new_indexes = list(filter(
                    lambda index:
                        not(index[0] < 0 or index[0] >= self.height or (
                            index[1] == c and index[0] < len(row) and c == r))
                        and
                        not(index[1] < 0 or index[1] >= self.height or (
                            index[0] <= r and index[1] >= len(row))),
                        edge_indexes
                        ))

                item.neighbors = list(map(
                    lambda index:
                        (item, graph_list_representation[index[0]][index[1]]),
                        new_indexes
                        )
                    )

                graph.add_edges_from(item.neighbors)

        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()

    # Board generation for diamond boards
    def gen_diamond_board(self, initial_empty):
        graph_list_representation = []

        for x in range(self.height):
            graph_list_representation.append(
                    [Peghole('filled') for _ in range(self.height)]
                )

        # Removes peg contents for each coordinate of initial holes
        for empty_peg in initial_empty:
            xpos = empty_peg[0]
            ypos = empty_peg[1]
            graph_list_representation[xpos][ypos].content = 'empty'

        self.contents = graph_list_representation
