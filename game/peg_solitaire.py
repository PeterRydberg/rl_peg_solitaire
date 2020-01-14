from Board import Board


def main():
    triangle_board = Board('triangle', 5)
    print(triangle_board.contents[2][2].content)

    diamond_board = Board('diamond', 2)
    print(diamond_board.contents[1][0].content)

    failboard = Board('kjhdsf', 3)
    print(failboard.contents[1][1].content)


if __name__ == "__main__":
    main()
