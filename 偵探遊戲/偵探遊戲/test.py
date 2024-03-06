import random

# Define some constants
DECK_SIZE = 52
SUITS = ["hearts", "clubs", "diamonds", "spades"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# Define a class to represent a card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit

# Define a function to create a deck of cards
def create_deck():
    deck = []
    for suit in SUITS:
        for rank in RANKS:
            deck.append(Card(suit, rank))
    return deck

# Define a function to shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Define a function to deal cards to the players
def deal_cards(deck, players):
    for player in players:
        player.hand = [deck.pop(0), deck.pop(0)]

# Define a function to calculate the score of a hand
def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        if card.rank == "A":
            aces += 1
        elif card.rank == "J" or card.rank == "Q" or card.rank == "K":
            score += 10
        else:
            score += int(card.rank)
    for i in range(aces):
        if score + 10 <= 21:
            score += 10
    return score

# Define a function to determine whether the player won
def player_won(hand, bank):
    return calculate_score(hand) > bank

# Define a function to play a round of the game
def play_round(deck, players, bank):
    # Deal the cards
    deal_cards(deck, players)
    
    # Show the hands
    for player in players:
        print(f"{player.name}'s hand: {player.hand}")
    
    # Determine the winner
    winner = None
    for player in players:
        if player_won(player.hand, bank):
            winner = player
            break
    
    # Pay the winner
    if winner:
        print(f"{winner.name} wins!")
        bank -= calculate_score(winner.hand)
        winner.balance += bank
        print(f"{winner.name}'s balance: {winner.balance}")
    else:
        print("The banker wins!")
        bank += 1
        print(f"The banker's balance: {bank}")
    
    return bank

# Define a function to play the game
def play_game(num_players):
    # Create the deck
    deck = create_deck()
    
    # Shuffle the deck
    deck = shuffle_deck(deck)
    
    # Define the players
    players = []
    for i in range(num_players):
        name = input(f"Enter player {i+1}'s name: ")
        players.append(Player(name))
    
    # Define the bank
    bank = 100
    
    # Play the game
    while bank > 0 and len(players) > 1:
        bank = play_round(deck, players, bank)
    
    # Show the final scores
    print("Final scores:")
    for player in players:
        print(f"{player.name}: {player.balance}")

# Define a class to represent a player
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.balance = 0

# Start the game
play_game(2)


