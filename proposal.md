# Title
Bet the House

## Repository
<https://github.com/salmoncave/bet-the-house>

## Description
Bet the House is a text-based Blackjack simulator game.

## Features
- Blackjack Deck
	- A list variable will contain all standard playing cards as objects with variables for the name, suit, and point total. Objects are removed from the list whenever randomly accessed, and the list will reset to original state at the end of each round
- Player Money System
	- The player’s money will be represented by an integer associated with and controlled by the player’s betting choices. Required bets are raised each round by tracking the current round and using it inside a formula to calculate the minimum buy-in.
- Ascii Art Rendering
	- Only the four suits and thirteen values of a standard playing card deck need to be acquired as Ascii art inputs. A card’s rendering will then be determined by its suit and name variables in the card class.

## Challenges
- Further research and investigation into the input() function will be utilized to properly time input events for actions that are appropriate for each possible game state.
- This project will require further practice with OOP in python.
- Basic ASCII art generation will be researched to see if it can be implemented as a basic graphical element. 

## Outcomes
Ideal Outcome:
- An ideal product would include a short blackjack game with scaling money costs and a simple difficulty ramping system.  The game would ideally also display ASCII art to represent each card.

Minimal Viable Outcome:
- The minimum viable outcome would be a much more simple program that simulates a single hand of Blackjack at a time. This would not include art, betting  or game structure.

## Milestones

- Week 1
  1. Research Blackjack Rules
  2. Research Ascii Art
  3. Build Card Object

- Week 2
  1. Implement Basic Deck and Round Logic
  2. Experiment with Player Money System and Ascii rendering

- Week 3
  1. Decide on Player Money System and Ascii implementation
  2. Plan for and begin finalization

- Week 4
  1. Finalize deliverables
  2. Perform final bug fixes
  3. Deliver final product 