import random

from .Card import Card

class DeckUNO(list):
    VALUES = [str(x) for x in range(0, 10)]
    COLORS = ["red", "yellow", "green", "blue"]

    def __init__(self):
        cards = [Card(x, y) for x in self.COLORS for y in self.VALUES]

        random.shuffle(cards)

        list.__init__(self, cards)
