# Bet The House

## Demo
Demo Video: <URL>

## GitHub Repository
GitHub Repo: <https://github.com/salmoncave/bet-the-house/tree/main>

## Description

    Bet The House is a simple Blackjack simulator. The events of the game are printed to the terminal and all of the player's actions(Hit, Stand, Double Down, Quit) are recorded using input commands. All actions in Blackjack, aside from splitting, are available and the program offers an accurate simulation of real life card mechanics. All of the logic is performed through various classes present in the single python file. With a large number of interconnected functions and dependent objects, extra care had to be taken to avoid creating two-way dependencies. The GameObject class handles the primary gameplay and is responsible for assigning a single card shoe to both the dealer and the player to guarentee the odds present in real life.
    
    The Card Shoe object generates Standard Decks which each contain the 52 cards present in a typical standard deck. To replicate the number of decks used in an average Blackjack game and their shuffling, 6 standard decks are generated and will completely regenerate if over 75% of the shoe has been drawn. Drawing a card from the shoe will completely remove them from the shoe, rendering that specific card unable to be drawn again even if other cards share same suit/value combination. The dealer also operates on the deterministic actions that a dealer must follow in Blackjack, hitting on anything below 17. Each entity, player and dealer, have the ability to decide the value of aces as they are considered worth either 1 or 11 points. Aces were assigned a default value of 11 to help streamline the case in which either entity hits a natural blackjack and no decision is made for the value. 
    
    Aces as a whole proved problematic, especially when multiple aces were involved. While this implementation worked well, the value for each ace does have to be manually determined each round. While a single simple solution could not be found, ideally the player would only have to chose an ace value if and when they would bust with an 11 value ace to avoid continuous inputs.