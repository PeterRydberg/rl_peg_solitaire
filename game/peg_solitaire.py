from PegGame import PegGame


def main():

    try:
        newGame = PegGame(
            'triangle',
            6,
            live_update_frequency=2,
            display_game=True
            )
        states = newGame.try_move((3, 3), 4)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
