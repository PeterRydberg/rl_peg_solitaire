from BoardGraph import BoardGraph
from Peghole import Peghole

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
                live_update_frequency
            )

    def generate_board(self, initial_empty):
        if(self.board_type == 'triangle'):
            if(not initial_empty):
                initial_empty = self.get_center()

            self.gen_triangle_board(initial_empty)
        elif(self.board_type == 'diamond'):
            if(not initial_empty):
                initial_empty = self.get_center()

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
                        self.board_content[index[0]][index[1]],
                        neighbors
                    )
                )

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
