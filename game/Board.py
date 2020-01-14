from Peg import Peg


class Board:
    def __init__(self, board_type, height, initial_hole=1):
        self.board_type = board_type
        self.height = height
        self.contents = self.generate_board(initial_hole)

    def generate_board(self, initial_hole):
        if(self.board_type == 'triangle'):
            return self.gen_triangle_board(initial_hole)
        elif(self.board_type == 'diamond'):
            return self.gen_diamond_board(initial_hole)
        else:
            print("you goofed")

    def gen_triangle_board(self, initial_hole):
        for x in range(self.height):
            print(x)

        peg = Peg()
        return [peg]

    def gen_diamond_board(self, initial_hole):
        pass
