import splendor.ansi_escape_codes as ansi
import splendor.board as sds


def deck_display():
    board = sds.Board("data/cards.csv", False)
    decks = board._decks
    for deck in decks:
        deck.reverse()
    deckSizes = (len(board._decks[0]), len(board._decks[1]), len(board._decks[2]))

    print(f"{ansi.B_YELLOW} DECK 0:       DECK 1:       DECK 2:{ansi.RESET}")
    for i in range(max(deckSizes)):
        print(
            f"{decks[0][i] if i < deckSizes[0] else '         '}     "
            f"{decks[1][i] if i < deckSizes[1] else '         '}     "
            f"{decks[2][i] if i < deckSizes[2] else '         '}"
        )


def main():
    deck_display()


if __name__ == "__main__":
    main()
