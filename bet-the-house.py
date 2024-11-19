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

    def display_inventory(self):
        print(f"\n{self.entity_name} Currently Holds:")
        for card in self.inventory:
            print(card.name)
        print(f"\n{self.entity_name} Total Card Value: {self.current_card_value}\n")

    def _draw_cards_to_inventory(self, cards_drawn: int = 1):
        cards_to_add = self.gameshoe.draw_cards_from_shoe(cards_drawn)
        
        for card in cards_to_add:
            self.inventory.append(card)
            self.current_card_value += card.value
        
    def _update_current_card_value(self):
        new_card_value : int = 0
        
        for card in self.inventory:
            new_card_value += card.value
        
        self.current_card_value = new_card_value

    def clear_cards_from_inventory(self):
        self.inventory = []
        self.current_card_value = 0
    
    def deal_starting_hand(self):
        self._draw_cards_to_inventory(2)

class Dealer(Entity):
    
    def __init__(self):
        Entity.__init__(self)
        self.entity_name = "Dealer"
    
    def display_starting_cards(self):
        print(f"\n{self.entity_name} Currently Holds:\n" + self.inventory[0].name)
        print(f"\n{self.entity_name} Has 1 Card Face-Down")
        print(f"{self.entity_name} Total Known Card Value: {self.inventory[0].value}")

class Player(Entity):
   
    def __init__(self):
        Entity.__init__(self)
        self.entity_name: str = "Player"
        self.current_money: int = 0
        self.unrecognized_input_warning: str = "Invalid Input Detected, Please Try Again!\n"
        self.win_message : str = "\nCongrats, you've hit Blackjack! You Win: NOTHING\n"
        self.loss_message : str = "\nYou've Lost! Too Bad, Restart Game?\n"

    def _process_player_action(self, chosen_action: str):
        if chosen_action == "hit":
           self._player_hit()
        elif chosen_action == "stand":
            self._player_stand()
        elif chosen_action == "double down":
            self._player_double_down()
        elif chosen_action == "forfeit":
            self._player_forfeit
        elif chosen_action == "quit game":
            pass

    def _check_player_score(self):
        if self.current_card_value > 21:
            self._player_loss()
        elif self.current_card_value == 21:
            self._player_win()
        else:
            self.offer_player_action()
    
    def _player_win(self):
        print(self.win_message)
        self.display_inventory()

    def _player_loss(self):
        leave_msg = "Thanks for Playing, See Ya Later!"
        self.display_inventory()
        restart_choice : str = input(f"{self.loss_message}").lower()
        
        if restart_choice == "yes" or restart_choice == "y":
            play_game()
        elif restart_choice == "no" or restart_choice == "n":
            print(leave_msg)
        else:
            print(self.unrecognized_input_warning)
            
    def _display_player_money(self):
        print(f"{self.entity_name} Current Money: {self.current_money}\n")
    
    def _check_ace_values(self):
        #ace_name : str = "No Ace Chosen"
        #ace_msg : str = (f"\nPlease type either '1' or '11' for the value of {ace_name}\n")
        
        for card in self.inventory:
            if card.type == "Ace":
                ace_name = card.name
                ace_value = input(f"\nType either '1' or '11' for the value of {ace_name}\n").lower()
                if ace_value == "11":
                    card.value = 11
                if ace_value == "1":
                    card.value = 1
                else:
                    print(self.unrecognized_input_warning)
                    self._check_ace_values(self)
        
        self._update_current_card_value()

    def _player_hit(self):
        self._draw_cards_to_inventory(1)
        self._check_ace_values()
        self._check_player_score()
    
    def _player_double_down(self):
        pass

    def _player_forfeit(self):
        pass
    
    def _player_stand(self):
        pass

    def offer_player_action(self):
        self.display_inventory()
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

def initialize_game(dealer: Dealer, player: Player, shoe: DealingShoe, starting_money: int = 500):
    player.gameshoe = shoe
    player.current_money = starting_money
    
    dealer.gameshoe = shoe

    welcome_msg : str = ("\n" + "\n" + "\n"
                        "--------------------------------------------\n" +
                        "Welcome to the Digital Arts Casino!\n" +
                        "You can't waste real money here, but at least you can pretend like you're not wasting your time!\n" +
                        "Let's get started shall we? Here we go!\n"
                        "--------------------------------------------\n")
    dealing_msg : str = "\nDealing Cards...\n"
    generation_msg : str = "Shuffling Shoe...\n"

    print(welcome_msg)
    print(dealing_msg)  
    print(generation_msg)

def check_natural_blackjack(dealer: Dealer, player: Player):
    message_type : str = "No message set, supply gameplay message"
    is_natural_game : bool = True

    if player.current_card_value == 21 and dealer.current_card_value == 21:
        message_type = "tied"
    elif player.current_card_value == 21 and dealer.current_card_value != 21:
        message_type = "naturalwin"
    elif player.current_card_value != 21 and dealer.current_card_value == 21:
        message_type = "naturalloss"
    else:
        message_type = "nonatural"
        is_natural_game = False

    print(display_gameplay_message(message_type))
    if is_natural_game:
        display_held_cards(dealer, player)
    
    return is_natural_game

def play_round(dealer: Dealer, player: Player, shoe: DealingShoe):
    dealer.deal_starting_hand()
    player.deal_starting_hand()
    if not check_natural_blackjack(dealer, player):
        dealer.display_starting_cards()
        player.offer_player_action()

def display_held_cards(dealer: Dealer, player: Player):
    dealer.display_inventory()
    player.display_inventory()
            
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