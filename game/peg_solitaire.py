from Board import Board


def main():

    try:
        triangle_board = Board('triangle', 3)
        print(triangle_board.board_content[1][1].content)

        diamond_board = Board('diamond', 3)
        print(diamond_board.board_content[1][0].content)

        failboard = Board('kjhdsf', 3)
        print(failboard.board_content[1][1].content)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()
