import random
import pprint
from enum import Enum

# May not need, currently deprecated. Can remove if enum becomes useless
class CardSuit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

class PlayingCard():

    def __init__(self, suit: str, card_type: str):
        card_types = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack","Queen","King","Ace"]
        card_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]

        self.suit : str = suit.lower().capitalize()
        self.type : str = card_type
        self.value : int = self._calculate_card_value(card_type)
        self.name : str = (f"{self.type} of {self.suit}")

    def _calculate_card_value(self, card_type: str):
        face_cards = ["Jack", "Queen", "King"]
        if card_type == "Ace":
            return 11
## Ace value set to 11 for now, TODO: add input to choose 1 or 11 after game structure implemented
        if card_type not in face_cards:
            return int(card_type)
        else:
            return 10

class StandardDeck():
    
    def __init__(self):
        
        self.deck : list = self._generate_standard_deck()
        
    
    def _generate_standard_deck(self):
        card_types = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack","Queen","King","Ace"]
        card_suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        playing_deck : list = []
        test_card_names: list = []

        for suit in card_suits:
            for type in card_types:
                card = PlayingCard(suit= suit, card_type= type)
                playing_deck.append(card)
                test_card_names.append(card.name)
        return test_card_names
    
    def pick_random_card(self):
        random_card = random.choice(self.deck)
        self.deck.remove(random_card)
    

def main():
    testdeck = StandardDeck
    pprint.pprint(testdeck._generate_standard_deck(testdeck))

if __name__ == "__main__":
    main()