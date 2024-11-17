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

        self.suit : str = suit.lower().capitalize()
        self.type : str = card_type
        self.value : int = self._calculate_card_value(card_type)
        self.name : str = (f"{self.type} of {self.suit}")

    def _calculate_card_value(self, card_type: str):
        face_cards : list[str] = ["Jack", "Queen", "King"]
        if card_type == "Ace":
            return 11
## Ace value set to 11 for now, TODO: add input to choose 1 or 11 after game structure implemented
        if card_type not in face_cards:
            return int(card_type)
        else:
            return 10

#Generates standard deck
class StandardDeck():
    
    def __init__(self):
        
        self.deck : list[PlayingCard] = self._generate_standard_deck()
    
    def _generate_standard_deck(self):
        card_types : list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10","Jack","Queen","King","Ace"]
        card_suits : list[str] = ["Clubs", "Diamonds", "Hearts", "Spades"]
        playing_deck : list[PlayingCard] = []

        for suit in card_suits:
            for type in card_types:
                card = PlayingCard(suit= suit, card_type= type)
                playing_deck.append(card)
       
        return playing_deck

class DealingShoe():

    def __init__(self):

        self.total_decks : int = 3
        self.card_shoe : list[PlayingCard] = self._generate_card_shoe(self.total_decks)

    def _generate_card_shoe(self, decks: int):
        shoe : list[PlayingCard] = []
        
        for deck in range(decks):
            shoe.extend(StandardDeck().deck)
        
        return shoe
    
    def draw_cards_from_shoe(self, cards_to_draw : int = 1):
        drawn_cards : list[PlayingCard] = []
        
        for cards in range(cards_to_draw):
            random_card : PlayingCard = random.choice(self.card_shoe)
            
            drawn_cards.append(random_card)
            self.card_shoe.remove(random_card)
        
        return drawn_cards

    def draw_full_shoe(self):
        pass

    def _regenerate_shoe(self, regen_threshold: int = 25):
        pass

    def interpret_cards_to_text(self, cards : list[PlayingCard]):
        interpreted_cards : list[str] = []
        
        for card in cards:
            interpreted_cards.append(card.name)

        return interpreted_cards


## Starts gameplay structure, called by main
def play_game():
    ''' testdeck = StandardDeck()
    print_range = range(26)
    for i in print_range:
        print(testdeck.pick_random_card().name)
    print("---------------------------------------------------")
    for n in print_range:
        print(testdeck.pick_random_card().name) '''
    testshoe = DealingShoe()
    pprint.pprint(testshoe.interpret_cards_to_text(testshoe.draw_cards_from_shoe(5)))

def main():
    play_game()

if __name__ == "__main__":
    main()