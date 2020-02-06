from .Board import Board
from enum import Enum


class PegGame:
    def __init__(
        self,
        board_type,
        board_size,
        initial_empty={},
        live_update_frequency=2,
        display_game=False,
        game_name=None
    ):
        self.display_game = display_game

        self.board = Board(
            board_type,
            board_size,
            initial_empty,
            live_update_frequency,
            self.display_game
        )

        if(self.display_game):
            self.game_name = game_name
            self.show_graph()

        # if(board_type == "triangle"):
        #     self.directions = DirectionsTriangle()
        # elif(board_type == "diamond"):
        #     self.directions = DirectionsDiamond()

    def try_move(self, peghole_index, direction):
        legal_moves = self.get_legal_moves()
        peghole = self.board.board_content[peghole_index[0]][peghole_index[1]]

        # If there are legal moves and the one chosen is legal
        if(legal_moves and (peghole, direction) in legal_moves):
            self.make_move((peghole, direction))

        return (self.board.board_content, self.get_legal_moves())

    def make_move(self, move):
        (peghole, direction) = move

        # Updates pegs to be changed for clear visuals
        if(self.display_game):
            peghole.content = "selected"
            peghole.neighbors[direction].content = "jump"
            self.update_graph()

        # Actually moves the pegs
        peghole.content = "empty"
        peghole.neighbors[direction].content = "empty"
        peghole.neighbors[direction].neighbors[direction].content = "filled"

        if(self.display_game):
            self.update_graph()

    def get_board_state(self):
        return self.board.board_content

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
        self.board.board_graph.show_graph(self.game_name)

    def update_graph(self):
        self.board.board_graph.live_update_graph(self.game_name)

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
