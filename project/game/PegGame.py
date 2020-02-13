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
    def try_move(self, move):
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

        return (self.board.board_content, self.get_legal_moves(True))

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
                        neighbor
                        and
                        neighbor.content != "empty"
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

    # Shows graph on demand
    def show_graph(self):
        self.board.board_graph.show_graph(self.game_name)

    # Updates graph
    def update_graph(self):
        self.board.board_graph.live_update_graph(self.game_name)

#    # Gets all possible board state permutations
#    def get_board_state_permutations(self):
#        states = []
#        pegholes = list(itertools.chain(*self.board.board_content))
#
#        def permutations(states, pegholes, current_permutation=[]):
#            #current_permutation = pegholes
#            if(len(pegholes) <= 1):
#                current_permutation
#                states.append(current_permutation)
#                pegholes[0].content = "empty"
#                states.append(current_permutation)
#            else:
#                for i in range(len(pegholes)):
#                    permutation_copy = current_permutation
#                    sub_array = pegholes[:i] + pegholes[i + 1:]
#
#                    peghole.content = "filled"
#                    #permutation_copy[i] = peghole
#                    permutations(states, sub_array, current_permutation)
#
#                    peghole.content = "empty"
#                    #permutation_copy[i] = peghole
#                    permutations(states, sub_array, current_permutation)

#        def permutations(states, pegholes, step=0):
#            if(step == len(pegholes)):
#                print(pegholes)
#                states.append(pegholes)
#            for i in range(step, len(pegholes)):
#                pegholes_copy = pegholes
#                pegholes_copy[step].content = "filled"
#                pegholes_copy[i].content = "empty"
#                permutations(states, pegholes_copy, step + 1)
#
#        permutations(states, pegholes)
#        return states

#                for i in range(step, len(pegholes)):
#                    state = []
#                    state.append(peghole.content = "filled")
#                    for nexthole in pegholes[:i:]:
#                        nexthole.content = "empty"
#                        self.permutations()
#
#                        state.append(state)
#                    states.append(state)

#    # Gets all possible state action pair permutations
#    def get_state_action_permutations(self):
#        pass


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
