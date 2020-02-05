from .BoardGraph import BoardGraph
from .Peghole import Peghole

import math


class Board:
    def __init__(
        self,
        board_type,
        height,
        initial_empty,
        live_update_frequency,
        display_game
    ):
        self.board_type = board_type
        self.height = height

        self.board_content = []
        self.generate_board(initial_empty)
        if(display_game):
            self.board_graph = BoardGraph(
                self.board_content,
                self.board_type,
                live_update_frequency
            )

    # Generate board types based on input type
    def generate_board(self, initial_empty):
        board_content = []
        if(not initial_empty):
            initial_empty = self.get_center()

        if(self.board_type == 'triangle'):
            board_content = self.gen_triangle_board(initial_empty)
        elif(self.board_type == 'diamond'):
            board_content = self.gen_diamond_board(initial_empty)
        else:
            raise ValueError("Board type must be triangle or diamond")

        self.board_content = board_content
        self.add_to_peghole_neighborhood()

    # Board generation for triangular boards
    def gen_triangle_board(self, initial_empty):
        board_content = []

        # Add pegholes and peghole rows to board
        for x in range(self.height):
            row = []
            for y in range(x + 1):
                peghole = self.gen_peghole(initial_empty, (x, y))
                row.append(peghole)
            board_content.append(row)

        return board_content

    # Board generation for diamond boards
    def gen_diamond_board(self, initial_empty):
        board_content = []

        # Add pegholes and peghole rows to board
        for x in range(self.height):
            row = []
            for y in range(self.height):
                peghole = self.gen_peghole(initial_empty, (x, y))
                row.append(peghole)
            board_content.append(row)

        return board_content

    def gen_peghole(self, initial_empty, coordinate):
        peghole = Peghole()
        peghole.coordinates = coordinate

        if(coordinate not in initial_empty):
            peghole.content = 'filled'
        else:  # Remove peg contents for each coordinate of initial holes
            peghole.content = 'empty'

        return peghole

    def add_to_peghole_neighborhood(self):
        for r, row in enumerate(self.board_content):
            for c, item in enumerate(row):

                # Triangle peghole edge indexes
                if(self.board_type == 'triangle'):
                    edge_indexes = [
                        (r-1, c),
                        (r, c+1),
                        (r+1, c+1),
                        (r+1, c),
                        (r, c-1),
                        (r-1, c-1)
                    ]

                    for index in edge_indexes:
                        if(  # If inside of board bounds
                            not(index[0] < 0 or index[0] >= self.height or (
                                    index[1] == c
                                    and index[0] < len(row)
                                    and c == r
                                ))
                            and
                            not(index[1] < 0 or index[1] >= self.height or (
                                index[0] <= r and index[1] >= len(row)))
                        ):  # Append the node to neighbors
                            item.neighbors.append(
                                self.board_content[index[0]][index[1]]
                            )
                        else:  # Else, append None
                            item.neighbors.append(None)

                # Diamond peghole edge indexes
                elif(self.board_type == 'diamond'):
                    edge_indexes = [
                        (r-1, c),
                        (r-1, c+1),
                        (r, c+1),
                        (r+1, c),
                        (r+1, c-1),
                        (r, c-1)
                    ]

                    for index in edge_indexes:
                        if(  # If inside of board bounds
                                not(index[0] < 0 or index[0] >= self.height)
                                and
                                not(index[1] < 0 or index[1] >= self.height)
                        ):  # Append the node to neighbors
                            item.neighbors.append(
                                self.board_content[index[0]][index[1]]
                                )
                        else:  # Else, append None
                            item.neighbors.append(None)

    # If empty holes are unspecified, default is center
    def get_center(self):
        x = 2
        y = 4 if(self.board_type == 'triangle') else 2
        return {
            (
                math.floor(self.height / x),
                math.floor(self.height / y)
            )
        }
