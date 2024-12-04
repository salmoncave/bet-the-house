import random
import time

class PlayingCard():

    def __init__(self, suit: str, card_type: str):

        self.suit : str = suit.lower().capitalize()
        self.type : str = card_type
        self.value : int = self._calculate_card_value(card_type)
        self.emoji : str = self._store_emoji_values(self.suit)
        self.name : str = (f"{self.type}{self.emoji}")

    def _calculate_card_value(self, card_type: str):
        face_cards : list[str] = ["J", "Q", "K"]
        if card_type == "A":
            return 11
## Ace value set to 11 initially for the purpose of checking natural blackjacks. Player chooses otherwise
        if card_type not in face_cards:
            return int(card_type)
        else:
            return 10

    def _store_emoji_values(self, suit: str):
        suit_art: dict[str] = {
            "Clubs" : "♣️",

            "Diamonds" : "♦️",

            "Hearts" : "♥️",

            "Spades" : "♠️", 
        }
        return_suit: str = suit_art[suit]

        return return_suit

class StandardDeck():
    
    def __init__(self):
        
        self.deck : list[PlayingCard] = self._generate_standard_deck()

#Generates standard deck
    def _generate_standard_deck(self):
        card_types : list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10","J","Q","K","A"]
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

    ''' Most Important Function in Shoe, Responsible for the following in order:
        - pick a random card from the cards available in the shoe
        - adds the picked card to the drawn cards array to return later
        - IMPORTANT: removes the card from the shoe so it cannot be drawn again, simulates card drawing randomization
        - IMPORTANT: checks if the shoe is at its regen threshold and regenerates the shoe, simulates shuffling'''

    def draw_cards_from_shoe(self, cards_to_draw : int = 1) -> list[PlayingCard] :
        drawn_cards : list[PlayingCard] = []
        
        for cards in range(cards_to_draw):
            random_card : PlayingCard = random.choice(self.card_shoe)

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
    
    def _slow_print(self, print_msg: str = "None", display_speed: int = 0.01):
        for character in print_msg:
           print(character, end="", flush= True)
           time.sleep(display_speed)

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
    
    def display_inventory(self):
        self._slow_print(print_msg = (f"\n{self.entity_name} Holds:\n"), display_speed = 0.05)
        for card in self.inventory:
            self._slow_print(print_msg = (f"{card.name}\n"), display_speed = 0.1)
        self._slow_print((f"\n{self.entity_name} Total Card Value: {self.current_card_value}\n"), 0.05)

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
        self._slow_print(f"\n{self.entity_name} Holds: {self.inventory[0].name}\n")
        self._slow_print(f"\n{self.entity_name} Holds 1 Additional Card Face-Down\n")
        self._slow_print(f"{self.entity_name} Total Known Card Value: {self.inventory[0].value}\n")
    
    def _has_aces(self):
        does_have_aces: bool = False
        
        for card in self.inventory:
            if card.type == "A":
                does_have_aces = True
        
        return does_have_aces

    def _get_aces(self):
        gathered_aces: list[PlayingCard] = []

        for card in self.inventory:
            if card.type == "A":
                gathered_aces.append(card)
        
        return gathered_aces
   
    def _decide_aces(self, gathered_aces: list[PlayingCard]):
        for ace in gathered_aces:
            ace.value = 1
    
    def _should_hit(self):
    
        if self.current_card_value >= 17:
            self._print_action_message("STAND")
            return False
        else:
            self._print_action_message("HIT")
            return True
        
    def _dealer_hit(self):
        self._draw_cards_to_inventory(1)
        self.display_inventory()
        self._process_score()
    
    def _print_action_message(self, action : str):
        self._slow_print("\nDealer will")
        self._slow_print(".... ", 0.35)
        self._slow_print(f"{action}\n", 0)

    def _process_score(self):
        if self.current_card_value > 21:
            if self._has_aces():
                self._decide_aces(self._get_aces())
                self._update_current_card_value()
        if self._should_hit():
            self._dealer_hit()

    def dealer_play(self):
        self.display_inventory()
        if self._should_hit():
            self._dealer_hit()

class Player(Entity):
   
    def __init__(self):
        Entity.__init__(self)
        self.entity_name: str = "Player"
        self.is_standing: bool = False
        self.has_lost: bool = False
        self.has_won: bool = False
        self.unrecognized_input_warning: str = "Invalid Input Detected, Please Try Again!\n"

    def _process_player_action(self, chosen_action: str):
        if chosen_action == "hit":
           self._player_hit()
        elif chosen_action == "stand":
            self._player_stand()
        elif chosen_action == "double down":
            self._player_double_down()
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
        self.display_inventory()
        self.has_won = True

    def _player_loss(self):
        self.display_inventory()
        self.has_lost = True
    
    def _check_ace_values(self):
        
        for card in self.inventory:
            if card.type == "A":
                ace_name = (f"{card.name}")
                self._slow_print("\nAce Detected!\n", 0.05)
                self.display_inventory()
                self._slow_print(f"\nCurrent hand value without {ace_name} = {(self.current_card_value - card.value)}\n")
                ace_value = input(f"\nType either '1' or '11' for the value of {ace_name}\n").lower()
                
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
            self.display_inventory()
            self.is_standing = True

    def _player_stand(self):
        self.is_standing = True

    def offer_player_action(self):
        self.display_inventory()
        prompt_msg : str = "\nAvailable Actions: 'hit', 'stand', 'double down', 'quit game'\n"
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

    def _display_gameplay_message(self, message_type: str, display_speed: int = 0.05):
        display_message: str = "No message set, supply gameplay message"
    
        match message_type:
            
            case "dealerwin":
                display_message = "\nOof too bad, looks like the dealer won this time.\n"
            case "dealing":
                display_message = "\nShuffling Shoe...\n" + "\nDealing Cards...\n"
            case "naturalloss":
                display_message = "\nOof, it looks like the Dealer got a natural. You'll get 'em next time Champ!\n"
            case "naturalwin":
                display_message= "\nWow you're a natural! Congratulations, you win: NOTHING.\n" 
            case "nonatural":
                display_message = "\nLooks like no one's a natural here today, play will continue.\n"
            case "playerwin": 
                display_message = "\nWow you've won, congradulations! You've won: NOTHING\n"
            case "scores":
                display_message = (
                f"\nPlayer Score: {self.player.current_card_value}\n" +
                f"Dealer Score: {self.dealer.current_card_value}\n"
                )
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
                casino_name + "\n")
            case "start":
                display_message = (
                "You can't waste real money here, but at least you can pretend like you're not wasting your time!\n" +
                "Let's get started shall we?\n"
                "--------------------------------------------\n")

        for character in display_message:
            print(character, end="", flush= True)
            time.sleep(display_speed)

    def _natural_blackjack(self, dealer: Dealer, player: Player):
        message_type : str = "NONE"
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
        self._display_gameplay_message("scores")
        if self.player.current_card_value > self.dealer.current_card_value or self.dealer.current_card_value > 21:
            self._display_gameplay_message("playerwin")
        else:
            self._display_gameplay_message("dealerwin")
    
    def _offer_player_restart(self):
        leave_msg = "Thanks for Playing, See Ya Later!"
        restart_choice : str = input("\nPlay Again?\n").lower()
        
        if restart_choice == "yes" or restart_choice == "y":
            play_game()
            del self
        elif restart_choice == "no" or restart_choice == "n":
            print(leave_msg)
        else:
            print("Input Not Recognized!")
            self._offer_player_restart()
    
    def _play_round(self):
        dealer : Dealer = self.dealer
        player : Player = self.player
        
        dealer.deal_starting_hand()
        player.deal_starting_hand()

        if self._natural_blackjack(dealer, player):
            self._offer_player_restart()
            return

        dealer.display_starting_cards()
        player.offer_player_action()

        if player.has_won:
            self._display_gameplay_message("playerwin")
        elif player.has_lost:
            self._display_gameplay_message("dealerwin")
        elif player.is_standing:
            print("\nPlayer Standing, Dealer Action")
            dealer.dealer_play()
            self._resolve_round_scores()
        else:
            print("INVALID GAMESTATE, OFFERING RESTART")
        self._offer_player_restart()
    
    def start_game(self, display_start_msg: bool = False):
        if display_start_msg:
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self._display_gameplay_message("welcome", 0.001)
            self._display_gameplay_message("start")
        self._display_gameplay_message("dealing")

        self._play_round()

def play_game(does_display_start_msg : bool = False):
    player : Player = Player()
    dealer : Dealer = Dealer()
    shoe : DealingShoe = DealingShoe()
    
    game_object : GameplayObject = GameplayObject(player= player, dealer= dealer, shoe= shoe)

    game_object.start_game(does_display_start_msg)


def main():
    play_game(does_display_start_msg = True)

if __name__ == "__main__":
    main()