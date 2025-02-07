import splendor.ansi_escape_codes as ansi
import splendor.board as sds

def deck_display():
    board = sds.Board('data/cards.csv')
    board_noshuffle = sds.Board('data/cards.csv', False)
    for i in range(len(board._decks)):
        print(f"{ansi.B_YELLOW}LEVEL {i + 1}{ansi.RESET}")
        for j in range(len(board._decks[i])):
            print(f"{board._decks[i][j]}    {board_noshuffle._decks[i][j]}")


def main():
    deck_display()


if __name__ == '__main__':
    main()