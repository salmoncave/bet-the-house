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
## Ace value set to 11 initially for the purpose of checking natural blackjacks. Player chooses otherwise
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
        self.gameshoe : DealingShoe
        self.inventory : list[PlayingCard] = []
        self.current_card_value : int = 0

    def _display_inventory(self):
        print(f"\n{self.entity_name} Currently Holds:")
        for card in self.inventory:
            print(card.name)
        print(f"\n{self.entity_name} Total Card Value: {self.current_card_value}\n")

    def add_cards_to_inventory(self, cards_to_add: list[PlayingCard]):
        for card in cards_to_add:
            self.inventory.append(card)
            self.current_card_value += card.value


    def clear_cards_from_inventory(self):
        self.inventory = []
        self.current_card_value = 0

class Dealer(Entity):
    
    def __init__(self):
        Entity.__init__(self)
        self.entity_name = "Dealer"
    
    def deal_starting_hands(self):
        pass

class Player(Entity):
   
    def __init__(self):
        Entity.__init__(self)
        self.entity_name: str = "Player"
        self.current_money: int = 0
        self.unrecognized_input_warning: str = "Invalid Input Detected, Please Try Again!\n"
        self.loss_message : str = "You've Lost! Too Bad, Restart Game?\n"

    def _process_player_action(self, chosen_action: str):
        if chosen_action == "hit":
            added_cards: list [PlayingCard] = self.gameshoe.draw_cards_from_shoe(1)
            for card in added_cards:
                if card.type == "Ace":
                    self._choose_ace_value(ace_card = card)
            self.add_cards_to_inventory(cards_to_add= added_cards)
            self._check_player_score()
        elif chosen_action == "stand":
            pass
        elif chosen_action == "double down":
            self.add_cards_to_inventory(self.gameshoe.draw_cards_from_shoe(2))
            self._check_player_score()
        elif chosen_action == "forfeit":
            pass
        elif chosen_action == "quit game":
            pass

    def _check_player_score(self):
        if self.current_card_value > 21:
            self._player_loss()
        else:
            self.offer_player_action()
    
    def _player_loss(self):
        leave_msg = "Thanks for Playing, See Ya Later!"
        restart_choice : str = input(f"{self.loss_message}").lower()
        
        if restart_choice == "yes" or restart_choice == "y":
            play_game()
        elif restart_choice == "no" or restart_choice == "n":
            print(leave_msg)
        else:
            print(self.unrecognized_input_warning)
            
    def _display_player_money(self):
        print(f"{self.entity_name} Current Money: {self.current_money}\n")
    
    def _choose_ace_value(self, ace_card : PlayingCard, from_hand : bool = False):
        if from_hand:
            ace_msg : str = "\nType '1' or '11' for the value of the Ace in hand"
        else:
            ace_msg : str = "\nYou've been dealt and Ace! Please type either '1' or '11' for the Ace's value\n"
        ace_value : int = input(f"{ace_msg}").lower()
        if ace_value == "11":
            ace_card.value = 11
        if ace_value == "1":
            ace_card.value = 1
        else:
            print(self.unrecognized_input_warning)
            self._choose_ace_value(ace_card)

    def offer_player_action(self):
        self._display_inventory()
        prompt_msg : str = "Available Actions: 'hit', 'stand', 'double down', 'forfeit', 'quit game'\n"
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


'''---------- GAMEPLAY FUNCTIONS -----------'''

def interpret_card_names_to_text(cards : list[PlayingCard]) -> list[str] :
    interpreted_cards : list[str] = []
    interpreted_cards.clear()

    for card in cards:
            interpreted_cards.append(card.name)

    return interpreted_cards

def play_round(dealer: Dealer, player: Player, shoe: DealingShoe):
    dealer.deal_starting_hands()
    check_natural_blackjack(dealer, player)

def initialize_game(dealer: Dealer, player: Player, shoe: DealingShoe, starting_money: int = 500):
    player.gameshoe = shoe
    player.current_money = starting_money
    
    dealer.gameshoe = shoe

    welcome_msg : str = ("\n" + "\n" + "\n"
                        "--------------------------------------------\n" +
                        "Welcome to the Digital Arts Casino!\n" +
                        "You can't earn real money here, but at least you can pretend like you're not wasting your time!\n" +
                        "Let's get started shall we? Here we go!\n"
                        "--------------------------------------------\n")

    print(welcome_msg)

def check_natural_blackjack(dealer: Dealer, player: Player):
    if player.current_card_value == 21 and dealer.current_card_value == 21:
        print(display_gameplay_message("tied"))
    elif player.current_card_value == 21 and dealer.current_card_value != 21:
        print(display_gameplay_message("naturalwin"))
    elif player.current_card_value != 21 and dealer.current_card_value == 21:
        print(display_gameplay_message("naturalloss"))
    else:
        print(display_gameplay_message("nonatural"))
            
def display_gameplay_message(message_type: str):
    display_message: str = "No message set, supply gameplay message"
    
    match message_type:
        case "tied": 
            display_message = "It looks like you've both got naturals, we've got a stand-off! No one wins and bets have been returned.\n"
        case "naturalwin":
            display_message= "Wow you're a natural! Congratulations, you win NO REWARD.\n" 
        case "naturalloss":
            display_message = "Oof, it looks like the Dealer got a natural. You'll get 'em next time Champ!\n"
        case "nonatural":
            display_message = "Looks like no one's a natural here today, play will continue.\n"

    return display_message


## Starts gameplay structure, called by main
def play_game():
    player : Player = Player()
    dealer : Dealer = Dealer()
    shoe : DealingShoe = DealingShoe()

    initialize_game(dealer, player, shoe)

    play_round(dealer, player, shoe)


def main():
    play_game()

if __name__ == "__main__":
    main()