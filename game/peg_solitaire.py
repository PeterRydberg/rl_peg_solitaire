from Board import Board


def main():
    board = Board('triangle', 5, (1, 2))
    print(board.contents[0].content)


if __name__ == "__main__":
    main()
