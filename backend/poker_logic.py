import random
from collections import Counter

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
    """Deal a hand of `hand_size` cards and update the remaining deck."""
    hand = deck[:hand_size]
    remaining_deck = deck[hand_size:]
    return hand, remaining_deck

# Replace selected cards in the hand
def replace_selected_cards(hand, deck, selected_indices):
    """
    Replace cards in `hand` at `selected_indices` with new cards from `deck`.
    Update the deck to reflect the removed cards.
    """
    new_cards = deck[:len(selected_indices)]  # Take as many new cards as needed
    remaining_deck = deck[len(selected_indices):]

    for i, index in enumerate(selected_indices):
        hand[index] = new_cards[i]  # Replace the selected cards with new cards

    return hand, remaining_deck

# Evaluate a hand
def evaluate_hand(hand):
    """
    Evaluate the poker hand and return an evaluation.
    Includes logic for pair, triple, quads, full house, straight, and flush.
    """
    # Split hand into ranks and suits
    ranks = [card.split(" ")[0] for card in hand]
    suits = [card.split(" ")[-1] for card in hand]
    
    # Convert ranks to numerical values for easier comparison
    rank_values = [RANKS.index(rank) for rank in ranks]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    
    # Sort ranks to check for straights
    rank_values.sort()

    # Check for flush
    is_flush = len(set(suits)) == 1

    # Check for straight
    is_straight = (
        len(set(rank_values)) == 5 and rank_values[-1] - rank_values[0] == 4
    )

    # Check for straight with Ace as low (A, 2, 3, 4, 5)
    if set(rank_values) == {0, 1, 2, 3, 12}:
        is_straight = True

    # Check hand combinations
    if is_straight and is_flush:
        return "Straight Flush!"
    elif 4 in rank_counts.values():
        return "Four of a Kind!"
    elif sorted(rank_counts.values()) == [2, 3]:
        return "Full House!"
    elif is_flush:
        return "Flush!"
    elif is_straight:
        return "Straight!"
    elif 3 in rank_counts.values():
        return "Three of a Kind!"
    elif list(rank_counts.values()).count(2) == 2:
        return "Two Pair!"
    elif 2 in rank_counts.values():
        return "Pair!"
    else:
        return "High Card!"

# Example: Main function to run logic
if __name__ == "__main__":
    # Create and shuffle the deck
    deck = create_deck()
    shuffled_deck = shuffle_deck(deck)

    # Deal an initial hand
    hand, remaining_deck = deal_hand(shuffled_deck)
    print("Player's initial hand:", hand)

    # Replace some cards (example: replace the 1st and 3rd cards)
    selected_indices = [0, 2]
    hand, remaining_deck = replace_selected_cards(hand, remaining_deck, selected_indices)

    print("Player's new hand:", hand)
    print("Remaining deck size:", len(remaining_deck))

    # Evaluate the hand
    print("Hand evaluation:", evaluate_hand(hand))
