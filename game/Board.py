from Peghole import Peghole
import math


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
            print("you goofed")

    # Board generation for triangular boards
    def gen_triangle_board(self, initial_empty):
        for x in range(self.height):
            self.contents.append(
                    [Peghole('filled') for _ in range(x + 1)]
                )

        # Removes peg contents for each coordinate of initial holes
        for empty_peg in initial_empty:
            self.contents[empty_peg[0]][empty_peg[1]].content = None

    # Board generation for diamond boards
    def gen_diamond_board(self, initial_empty):
        for x in range(self.height):
            self.contents.append(
                    [Peghole('filled') for _ in range(self.height)]
                )

        # Removes peg contents for each coordinate of initial holes
        for empty_peg in initial_empty:
            self.contents[empty_peg[0]][empty_peg[1]].content = None
