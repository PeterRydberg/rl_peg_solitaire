from Peghole import Peghole

import math

import networkx as nx
import matplotlib.pyplot as plt


class Board:
    def __init__(self, board_type, height, initial_empty={}):
        self.board_type = board_type
        self.height = height

        # If empty holes are unspecified, default is center
        if(not initial_empty):
            initial_empty = {
                (math.floor(self.height / 2), math.floor(self.height / 2))
                }
        self.board_content = []
        self.graph = nx.Graph()
        self.generate_board(initial_empty)

    def generate_board(self, initial_empty):
        if(self.board_type == 'triangle'):
            self.gen_triangle_board(initial_empty)
        elif(self.board_type == 'diamond'):
            self.gen_diamond_board(initial_empty)
        else:
            raise ValueError("Board type must be triangle or diamond")

    # Board generation for triangular boards
    def gen_triangle_board(self, initial_empty):
        board_content = []

        for x in range(self.height):
            row = []
            for y in range(x + 1):

                if((x, y) not in initial_empty):
                    row.append(Peghole('filled'))
                # Removes peg contents for each coordinate of initial holes
                else:
                    row.append(Peghole('empty'))
            board_content.append(row)

        self.board_content = board_content
        self.add_to_peghole_neighborhood()

    # Board generation for diamond boards
    def gen_diamond_board(self, initial_empty):
        board_content = []

        for x in range(self.height):
            row = []
            for y in range(self.height):

                if((x, y) not in initial_empty):
                    row.append(Peghole('filled'))
                # Removes peg contents for each coordinate of initial holes
                else:
                    row.append(Peghole('empty'))
            board_content.append(row)

        self.board_content = board_content
        self.add_to_peghole_neighborhood()

    def add_to_peghole_neighborhood(self):
        for r, row in enumerate(self.board_content):
            for c, item in enumerate(row):

                if(self.board_type == 'triangle'):
                    edge_indexes = [
                        (r-1, c),
                        (r, c+1),
                        (r+1, c+1),
                        (r+1, c),
                        (r, c-1),
                        (r-1, c-1)
                    ]

                    neighbors = list(filter(
                        lambda index:
                            not(index[0] < 0 or index[0] >= self.height or (
                                    index[1] == c
                                    and index[0] < len(row)
                                    and c == r
                                ))
                            and
                            not(index[1] < 0 or index[1] >= self.height or (
                                index[0] <= r and index[1] >= len(row))),
                            edge_indexes
                    ))

                elif(self.board_type == 'diamond'):
                    edge_indexes = [
                        (r-1, c),
                        (r-1, c+1),
                        (r, c+1),
                        (r+1, c),
                        (r+1, c-1),
                        (r, c-1)
                    ]

                    neighbors = list(filter(
                        lambda index:
                            not(index[0] < 0 or index[0] >= self.height)
                            and
                            not(index[1] < 0 or index[1] >= self.height),
                            edge_indexes
                    ))

                item.neighbors = list(map(
                    lambda index:
                        (item, self.board_content[index[0]][index[1]]),
                        neighbors
                    )
                )

                # Add to visual graph
                self.graph.add_edges_from(item.neighbors)

        nx.draw(self.graph, with_labels=True, font_weight='bold')
        plt.show()
