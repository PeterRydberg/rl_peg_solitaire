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

        if(board_type == "triangle"):
            self.directions = DirectionsTriangle
        elif(board_type == "diamond"):
            self.directions = DirectionsDiamond

    # Move attempt function
    def try_move(self, move, return_reward=False):
        peghole_index, direction_name = move
        legal_moves = self.get_legal_moves()
        peghole = self.board.board_content[peghole_index[0]][peghole_index[1]]
        direction = self.directions[direction_name].value

        def make_move(move):
            (peghole, direction) = move

            # Updates pegs to be changed for clear visuals
            if(self.display_game):
                peghole.content = "selected"
                peghole.neighbors[direction].content = "jump"
                self.update_graph()

            # Actually moves the pegs
            peghole.content = "empty"
            peghole.neighbors[direction].content = "empty"
            peghole.neighbors[direction].neighbors[direction].content = \
                "filled"

            if(self.display_game):
                self.update_graph()

        # If there are legal moves and the one chosen is legal
        if(legal_moves and (peghole, direction) in legal_moves):
            make_move((peghole, direction))

        # Returns with or without reward (for training purposes)
        if(return_reward is True):
            return ((
                self.get_reward(fixed_reward=True),
                self.board.board_content,
                self.get_legal_moves(True)
            ))

        return ((
            self.board.board_content,
            self.get_legal_moves(True)
        ))

    def get_board_state(self):
        return self.board.board_content

    # Returns all legal moves for the current board state
    def get_legal_moves(self, simplified=False):
        legal_moves = []
        for r, row in enumerate(self.board.board_content):
            for c, peghole in enumerate(row):
                for i, neighbor in enumerate(peghole.neighbors):
                    # If possible direct jump over adjacent node
                    if(
                        peghole.content != "empty"
                        and
                        neighbor
                        and
                        neighbor.content == "filled"
                        and
                        neighbor.neighbors[i]
                        and
                        neighbor.neighbors[i].content == "empty"
                    ):
                        if(simplified):
                            legal_moves.append(
                                ((r, c), self.directions(i).name)
                                )
                        else:
                            legal_moves.append(
                                (peghole, self.directions(i).value)
                            )

        return legal_moves

    # Calculates reward based on amount of pegs left
    def get_reward(self, fixed_reward=True):
        legal_moves = self.get_legal_moves()

        if(fixed_reward and len(legal_moves) < 1):
            amount = 0
            for row in self.board.board_content:
                for peghole in row:
                    amount += 1 if peghole.content == "empty" else 0
            return 5000 if amount == 1 else -5000
        else:
            reward = 0
            for row in self.board.board_content:
                for peghole in row:
                    reward += 10 if peghole.content == "empty" else 0
            return reward
        return 0

    # Shows graph on demand
    def show_graph(self):
        self.board.board_graph.show_graph(self.game_name)

    # Updates graph
    def update_graph(self):
        self.board.board_graph.live_update_graph(self.game_name)


# Legal directions for triangle boards
class DirectionsTriangle(Enum):
    UP = 0
    RIGHT = 1
    DOWN_RIGHT = 2
    DOWN = 3
    LEFT = 4
    UP_LEFT = 5


# Legal directions for diamond boards
class DirectionsDiamond(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN = 3
    DOWN_LEFT = 4
    LEFT = 5
