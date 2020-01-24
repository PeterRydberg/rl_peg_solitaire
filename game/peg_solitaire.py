from PegGame import PegGame


def main():

    try:
        newGame = PegGame(
            'triangle',
            7,
            live_update_frequency=20,
            display_game=True
            )
        print(newGame.get_legal_moves())
        states = newGame.make_move("down")
        print(states)
        newGame.show_graph()
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
