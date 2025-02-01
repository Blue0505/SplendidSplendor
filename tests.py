import splendid_data_structures as sds
import ansi_escape_codes as ansi


def deck_display():
    board = sds.Board('cards.csv')
    board_noshuffle = sds.Board('cards.csv', no_shuffle=False)
    for i in range(len(board.decks)):
        print(f"{ansi.B_YELLOW}LEVEL {i + 1}{ansi.RESET}")
        for j in range(len(board.decks[i])):
            print(f"{board.decks[i][j]}    {board_noshuffle.decks[i][j]}")


def main():
    deck_display()


if __name__ == '__main__':
    main()