import random

# Define suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Generate a deck of cards
def create_deck():
    return [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]

# Shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Deal cards to a player
def deal_hand(deck, hand_size=5):
    hand = deck[:hand_size]
    remaining_deck = deck[hand_size:]
    return hand, remaining_deck

# Example: Main function to run logic
if __name__ == "__main__":
    deck = create_deck()
    shuffled_deck = shuffle_deck(deck)
    hand, remaining_deck = deal_hand(shuffled_deck)
    
    print("Player's hand:", hand)
    print("Remaining deck size:", len(remaining_deck))
    

from collections import Counter

# Evaluate a hand (basic example for pairs)
def evaluate_hand(hand):
    ranks = [card.split(" ")[0] for card in hand]
    rank_counts = Counter(ranks)
    if 2 in rank_counts.values():
        return "Pair!"
    else:
        return "High card."