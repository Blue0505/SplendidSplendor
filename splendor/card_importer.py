import csv

from splendor.card import Card
from splendor.gem import Gem


def csv_import(filepath: str) -> list[list[Card]]:
    """Loads cards from a CSV file and returns three decks. These decks
    contain all level 1, level 2, and level 3 cards respectively.
    """
    csv_gem_names: dict[str, Gem] = {
        "white": Gem.WHITE,
        "blue": Gem.BLUE,
        "green": Gem.GREEN,
        "red": Gem.RED,
        "black": Gem.BLACK,
    }

    decks = [[] for _ in range(3)]
    with open(filepath) as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            points = int(row["points"]) if row["points"] else 0
            gem_type = csv_gem_names[row["gem-color"]]
            costs = (
                int(row["c-white"]) if row["c-white"] else 0,
                int(row["c-blue"]) if row["c-blue"] else 0,
                int(row["c-green"]) if row["c-green"] else 0,
                int(row["c-red"]) if row["c-red"] else 0,
                int(row["c-black"]) if row["c-black"] else 0,
            )
            decks[int(row["level"]) - 1].append(Card(points, gem_type, costs))
    return decks
