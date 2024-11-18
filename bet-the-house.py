import random
import pprint
from enum import Enum

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

class StandardDeck():
    
    def __init__(self):
        
        self.deck : list[PlayingCard] = self._generate_standard_deck()

#Generates standard deck
    def _generate_standard_deck(self):
        card_types : list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10","Jack","Queen","King","Ace"]
        card_suits : list[str] = ["Clubs", "Diamonds", "Hearts", "Spades"]
        playing_deck : list[PlayingCard] = []

        for suit in card_suits:
            for type in card_types:
                card = PlayingCard(suit= suit, card_type= type)
                playing_deck.append(card)
       
        return playing_deck

class DealingShoe():

    def __init__(self):

        self.total_decks : int = 4
        self.card_shoe : list[PlayingCard] = self._generate_card_shoe(self.total_decks)
        self.regen_threshold : float = (0.25 * (self.total_decks * 52))
        
    def _generate_card_shoe(self, decks: int):
        shoe : list[PlayingCard] = []
        
        for deck in range(decks):
            shoe.extend(StandardDeck().deck)

        return shoe
    
    def _regenerate_shoe(self):
        self.card_shoe.clear()
        self.card_shoe = self._generate_card_shoe(self.total_decks)
        print("----------------")
        print("SHOE RENEGERATED")
        print("----------------")

    ''' Most Important Function in Shoe, Responsible for the following in order:
        - pick a random card from the cards available in the shoe
        - adds the picked card to the drawn cards array to return later
        - IMPORTANT: removes the card from the shoe so it cannot be drawn again, simulates card drawing randomization
        - IMPORTANT: checks if the shoe is at its regen threshold and regenerates the shoe, simulates shuffling'''

    def draw_cards_from_shoe(self, cards_to_draw : int = 1) -> list[PlayingCard] :
        drawn_cards : list[PlayingCard] = []
        
        for cards in range(cards_to_draw):
            random_card : PlayingCard = random.choice(self.card_shoe)
            '''print(random_card.name)'''

            self.card_shoe.remove(random_card)
            drawn_cards.append(random_card)

            if len(self.card_shoe) <= self.regen_threshold:
                self._regenerate_shoe()
            
        return drawn_cards

class Entity():
    
    def __init__(self):
        self.entity_name : str = "Entity"
        self.inventory : list[PlayingCard] = []
        self.current_card_value : int = 0

    def _display_inventory(self):
        print(f"\n{self.entity_name} Currently Holds:")
        for card in self.inventory:
            print(card.name)
        print(f"\n{self.entity_name} Total Card Value: {self.current_card_value}")

    def add_cards_to_inventory(self, cards_to_add: list[PlayingCard]):
        for card in cards_to_add:
            self.inventory.append(card)
            self.current_card_value += card.value
        self._display_inventory()

    def clear_cards_from_inventory(self):
        self.inventory = []
        self.current_card_value = 0

class Dealer(Entity):
    
    def __init__(self):
        Entity.__init__(self)
        self.entity_name = "Dealer"

class Player(Entity):
   
    def __init__(self):
        Entity.__init__(self)
        self.entity_name: str = "Player"
        self.unrecognized_input_warning: str = "Player Input Not Recognized, Please Try Again\n"
        self.current_money: int = 0

    def offer_player_action(self):
        prompt_msg : str = "Available Actions: 'hit', 'stand', 'double down', 'forfeit', 'quit game\n"
        action_choice: str = input(f"{prompt_msg}").lower()

        if (action_choice == "hit" or 
            action_choice == "stand" or 
            action_choice == "double down" or 
            action_choice == "forfeit" or
            action_choice == "quit game"):

            self._process_player_action(action_choice)
        else:
            print(self.unrecognized_input_warning)
            self.offer_player_action()

    def _process_player_action(self, chosen_action: str):
        if chosen_action == "hit":
            self.add_cards_to_inventory(gameshoe.draw_cards_from_shoe(1))
            self._check_player_score()
        if chosen_action == "stand":
            pass
        if chosen_action == "double down":
            self.add_cards_to_inventory(gameshoe.draw_cards_from_shoe(2))
            self._check_player_score()
        if chosen_action == "forfeit":
            pass
        if chosen_action == "quit game":
            pass

    def _check_player_score(self):
        if self.current_card_value > 21:
            print("You lose! Too bad. See Ya Later!")
        else:
            self.offer_player_action()
    
    def _display_player_money(self):
        print(f"{self.entity_name} Current Money: {self.current_money}\n")

'''---------- GAMEPLAY FUNCTIONS -----------'''

def interpret_card_names_to_text(cards : list[PlayingCard]) -> list[str] :
    interpreted_cards : list[str] = []
    interpreted_cards.clear()

    for card in cards:
            interpreted_cards.append(card.name)

    return interpreted_cards


## Starts gameplay structure, called by main
def play_game():
    player : Player = Player()
    
    welcome_msg : str = ("\n" + "\n" + "\n"
                        "--------------------------------------------\n" +
                        "Welcome to the Digital Arts Casino!\n" +
                        "You can't earn real money here, but at least you can pretend like you're not wasting your time!\n" +
                        "Let's get started shall we? Here we go!\n"
                        "--------------------------------------------\n")

    print(welcome_msg)
    player.offer_player_action()

'''Gameshoe and dealer currently global variables for access, looking for another solution'''

gameshoe : DealingShoe = DealingShoe()
dealer : Dealer = Dealer()

def main():
    play_game()

if __name__ == "__main__":
    main()