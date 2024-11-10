import random
from enum import Enum

class CardSuit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

class PlayingCard():

    def __init__(self, suit: CardSuit, CardName: str):
        cardnames = {
        "1" : 1,
        "2" : 2,
        "3" : 3,
        "4" : 4,
        "5" : 5,
        "6" : 6,
        "7" : 7,
        "8" : 8,
        "9" : 9,
        "10" : 10,
        "J" : 10,
        "Q" : 10,
        "K" : 10,
        "A" : 11,
    }
        
        self.suit = suit
        self.name = CardName
        self.value = cardnames[CardName]

def main():
    testcard = PlayingCard(CardSuit.CLUBS, CardName= "J")
    print(testcard.name ,testcard.suit, testcard.value)

if __name__ == "__main__":
    main()