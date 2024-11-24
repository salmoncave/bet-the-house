import random

class PlayingCard():

    def __init__(self, suit: str, card_type: str):

        self.suit : str = suit.lower().capitalize()
        self.type : str = card_type
        self.value : int = self._calculate_card_value(card_type)
        self.name : str = (f"{self.type} of {self.suit}")
        self.ascii : str = self._store_ascii_values(self.suit, self.type)

    def _calculate_card_value(self, card_type: str):
        face_cards : list[str] = ["Jack", "Queen", "King"]
        if card_type == "Ace":
            return 11
## Ace value set to 11 initially for the purpose of checking natural blackjacks. Player chooses otherwise
        if card_type not in face_cards:
            return int(card_type)
        else:
            return 10

    def _store_ascii_values(self, suit: str, type: str):
        suit_art: dict[str] = {
            "Clubs" : """
       .+XX+.       
     .$&&&&&&X      
     +&&&&&&&&;     
     .&&&&&&&$      
  ;&&&&&&&&&&&&&&;  
 +&&&&&&&&&&&&&&&&; 
 +&&&&&&&&&&&&&&&&+ 
  +&&&&&+$X+&&&&&+  
        +&&+        
       ......       """,

            "Diamonds" : """                    
         &&         
       &&&&&&       
      &&&&&&&&      
    &&&&&&&&&&&&    
  &&&&&&&&&&&&&&&&  
    &&&&&&&&&&&&    
      &&&&&&&&      
       &&&&&&       
         &&         """,

            "Hearts" : """              
   &&&&&&  &&&&&&   
  &&&&&&&&&&&&&&&&  
 &&&&&&&&&&&&&&&&&& 
  &&&&&&&&&&&&&&&&  
   &&&&&&&&&&&&&&   
     &&&&&&&&&&     
       &&&&&&       
        &&&&        
                    """,

            "Spades" : """
        &&&&        
      &&&&&&&&      
    &&&&&&&&&&&&    
   &&&&&&&&&&&&&&   
  &&&&&&&&&&&&&&&&  
 &&&&&&&&&&&&&&&&&  
  &&&&&&&&&&&&&&&&  
    &&&  &&  &&&    
        &&&&        """, 
        }

        return_suit: str = suit_art[self.suit]

        return return_suit

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
            print(card.ascii)
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
    
    def _has_aces(self):
        does_have_aces: bool = False
        
        for card in self.inventory:
            if card.type == "Ace":
                does_have_aces = True
        
        return does_have_aces

#Need to fix ace gathering and processing
    def _get_aces(self):
        gathered_aces: list[PlayingCard] = []

        for card in self.inventory:
            if card.type == "Ace":
                gathered_aces.append(card)
        
        return gathered_aces
   
    def _decide_aces(self, gathered_aces: list[PlayingCard]):
        for ace in gathered_aces:
            ace.value = 1
    
    def _should_hit(self):
        if self.current_card_value >= 17:
            return False
        else:
            return True
        
    def _dealer_hit(self):
        self._draw_cards_to_inventory(1)
        self.display_inventory()
        self._process_score()

    def _process_score(self):
        if self._should_hit():
            self._dealer_hit()
        elif self.current_card_value == 21:
            pass
        elif self.current_card_value > 21:
            if self._has_aces():
                self._decide_aces(self._get_aces())

    def dealer_play(self):
        self.display_inventory()
        if self._should_hit():
            self._dealer_hit()

class Player(Entity):
   
    def __init__(self):
        Entity.__init__(self)
        self.entity_name: str = "Player"
        self.current_money: int = 0
        self.is_standing: bool = False
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

    def _round_end_score(self):
        does_end: bool = True

        if self.current_card_value > 21:
            self._player_loss()
        elif self.current_card_value == 21:
            self._player_win()
        else:
            does_end = False

        return does_end
    
    def _player_win(self):
        print(self.win_message)

##NEED FIX, DOES NOT WORK IN CURRENT GAME LOOP ANY LONGER
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
                print(f"\nCurrent card value without {ace_name} = {self.current_card_value - card.value}")
                ace_value = input(f"Type either '1' or '11' for the value of {ace_name}\n").lower()
                
                if ace_value == "11":
                    card.value = 11
                elif ace_value == "1":
                    card.value = 1
                else:
                    print(self.unrecognized_input_warning)
                    self._check_ace_values()
        
        self._update_current_card_value()

    def _player_hit(self):
        self._draw_cards_to_inventory(1)
        self._check_ace_values()
        if not self._round_end_score():
            self.offer_player_action()
    
    def _player_double_down(self):
        self._draw_cards_to_inventory(1)
        self._check_ace_values()
        if not self._round_end_score():
            self.is_standing = True

    def _player_forfeit(self):
        pass
    
    def _player_stand(self):
        self.is_standing = True

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

class GameplayObject():
    def __init__(self, dealer: Dealer, player: Player, shoe: DealingShoe) -> None:
        self.dealer : Dealer = dealer
        self.player : Player = player
        self.shoe : DealingShoe = shoe
        
        self.player.gameshoe = shoe
        self.dealer.gameshoe = shoe

    def _display_gameplay_message(self, message_type: str):
        display_message: str = "No message set, supply gameplay message"
    
        match message_type:
            
            case "dealerwin":
                display_message = "\nOof too bad, looks like the dealer won this time.\n"
            case "dealing":
                display_message = "Shuffling Shoe...\n" + "\nDealing Cards...\n"
            case "naturalloss":
                display_message = "Oof, it looks like the Dealer got a natural. You'll get 'em next time Champ!\n"
            case "naturalwin":
                display_message= "Wow you're a natural! Congratulations, you win NO REWARD.\n" 
            case "nonatural":
                display_message = "Looks like no one's a natural here today, play will continue.\n"
            case "playerwin": 
                display_message = "\nWow you've won, congradulations! You've earned: NOTHING\n"
            case "tied": 
                display_message = "It looks like you've both got naturals, we've got a stand-off! No one wins and bets have been returned.\n"
            case "welcome":
                casino_name: str = r""" 
 /$$$$$$$  /$$           /$$   /$$               /$$        /$$$$$$              /$$                     /$$$$$$                      /$$                     /$$ /$$
| $$__  $$|__/          |__/  | $$              | $$       /$$__  $$            | $$                    /$$__  $$                    |__/                    | $$| $$
| $$  \ $$ /$$  /$$$$$$  /$$ /$$$$$$    /$$$$$$ | $$      | $$  \ $$  /$$$$$$  /$$$$$$   /$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$$ /$$ /$$$$$$$   /$$$$$$ | $$| $$
| $$  | $$| $$ /$$__  $$| $$|_  $$_/   |____  $$| $$      | $$$$$$$$ /$$__  $$|_  $$_/  /$$_____/      | $$       |____  $$ /$$_____/| $$| $$__  $$ /$$__  $$| $$| $$
| $$  | $$| $$| $$  \ $$| $$  | $$      /$$$$$$$| $$      | $$__  $$| $$  \__/  | $$   |  $$$$$$       | $$        /$$$$$$$|  $$$$$$ | $$| $$  \ $$| $$  \ $$|__/|__/
| $$  | $$| $$| $$  | $$| $$  | $$ /$$ /$$__  $$| $$      | $$  | $$| $$        | $$ /$$\____  $$      | $$    $$ /$$__  $$ \____  $$| $$| $$  | $$| $$  | $$        
| $$$$$$$/| $$|  $$$$$$$| $$  |  $$$$/|  $$$$$$$| $$      | $$  | $$| $$        |  $$$$//$$$$$$$/      |  $$$$$$/|  $$$$$$$ /$$$$$$$/| $$| $$  | $$|  $$$$$$/ /$$ /$$
|_______/ |__/ \____  $$|__/   \___/   \_______/|__/      |__/  |__/|__/         \___/ |_______/        \______/  \_______/|_______/ |__/|__/  |__/ \______/ |__/|__/
               /$$  \ $$                                                                                                                                             
              |  $$$$$$/                                                                                                                                             
               \______/                                                                                                                                              
         """
                display_message = ("\n" + "\n" + "\n"
                        "--------------------------------------------\n" +
                        "Welcome to the\n" +
                        casino_name + "\n" +
                        "You can't waste real money here, but at least you can pretend like you're not wasting your time!\n" +
                        "Let's get started shall we? Here we go!\n"
                        "--------------------------------------------\n")

        print(display_message)

    def _natural_blackjack(self, dealer: Dealer, player: Player):
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

        self._display_gameplay_message(message_type)
    
        return is_natural_game
    
    def _display_all_cards(self):
        self.dealer.display_inventory()
        self.player.display_inventory()
    
    def _resolve_round_scores(self):
        if self.player.current_card_value > self.dealer.current_card_value or self.dealer.current_card_value > 21:
            self._display_gameplay_message("playerwin")
        else:
            self._display_gameplay_message("dealerwin")

    def start_game(self):
        self._display_gameplay_message("welcome")
        self._display_gameplay_message("dealing")

        self._play_round()
    
    def _play_round(self):
        dealer : Dealer = self.dealer
        player : Player = self.player
        
        dealer.deal_starting_hand()
        player.deal_starting_hand()
        if not self._natural_blackjack(dealer, player):
            dealer.display_starting_cards()
            player.offer_player_action()
        if player.is_standing:
            print("Player Standing, Dealer Action")
            dealer.dealer_play()
            self._resolve_round_scores()
        else:
            self._display_all_cards()
            print("Round Ended")

#CURRENTLY DEPRECATED
def interpret_card_names_to_text(cards : list[PlayingCard]) -> list[str] :
    interpreted_cards : list[str] = []
    interpreted_cards.clear()

    for card in cards:
            interpreted_cards.append(card.name)

    return interpreted_cards

## Starts gameplay structure, called by main
## MAY MOVE GAMEPLAY AND ALL OBJECTS TO GameObject Class AND CALL GameObject.play_game on main
def play_game():
    player : Player = Player()
    dealer : Dealer = Dealer()
    shoe : DealingShoe = DealingShoe()
    
    game_object : GameplayObject = GameplayObject(player= player, dealer= dealer, shoe= shoe)

    game_object.start_game()


def main():
    play_game()

if __name__ == "__main__":
    main()