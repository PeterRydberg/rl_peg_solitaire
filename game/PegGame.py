from Board import Board
from enum import Enum


class PegGame:
    def __init__(
        self,
        board_type,
        board_size,
        initial_empty={},
        live_update_frequency=2,
        display_game=False
    ):
        self.display_game = display_game
        # if(board_type == "triangle"):
        #     self.directions = DirectionsTriangle()
        # elif(board_type == "diamond"):
        #     self.directions = DirectionsDiamond()

        self.board = Board(
            board_type,
            board_size,
            initial_empty,
            live_update_frequency,
            self.display_game
        )

    def make_move(self, direction):
        pass

    def get_legal_moves(self):
        legal_moves = []
        for row in self.board.board_content:
            for peghole in row:
                for i, neighbor in enumerate(peghole.neighbors):
                    # If possible direct jump over adjacent node
                    if(
                        neighbor
                        and
                        neighbor.content != "empty"
                        and
                        neighbor.neighbors[i]
                        and
                        neighbor.neighbors[i].content == "empty"
                    ):
                        legal_moves.append((peghole, i))
        return legal_moves

    def show_graph(self):
        self.board.board_graph.display_graph()

    # Legal directions for triangle boards
    class DirectionsTriangle(Enum):
        up = 0
        right = 1
        down_right = 2
        down = 3
        left = 4
        up_left = 5

    # Legal directions for diamond boards
    class DirectionsDiamond(Enum):
        up = 0
        up_right = 1
        right = 2
        down = 3
        down_left = 4
        left = 5
