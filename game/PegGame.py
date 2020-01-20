from Board import Board


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

        self.board = Board(
            board_type,
            board_size,
            initial_empty,
            live_update_frequency,
            self.display_game
        )

    def show_graph(self):
        self.board.board_graph.display_graph()
