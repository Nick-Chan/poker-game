import random
from collections import Counter

# Define suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Global betting counter
STARTING_MONEY = 100

# Payouts for hand evaluations
PAYOUTS = {
    "Straight Flush!": 50,
    "Four of a Kind!": 25,
    "Full House!": 15,
    "Flush!": 10,
    "Straight!": 8,
    "Three of a Kind!": 5,
    "Two Pair!": 3,
    "Pair!": 1,
    "High Card!": 0
}

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

# Main function
def main():
    global STARTING_MONEY
    money = STARTING_MONEY
    deck = shuffle_deck(create_deck())
    free_redeal_used = False

    print(f"Welcome to Poker! Starting money: ${money}")

    while True:
        if len(deck) < 5:  # Reshuffle if deck is too small
            print("Shuffling the deck...")
            deck = shuffle_deck(create_deck())
            free_redeal_used = False

        # Deal cards
        print("\nDealing cards...")
        if money >= 10:
            money -= 10
            hand, deck = deal_hand(deck)
            print(f"Your hand: {hand}")
        else:
            print("Not enough money to deal cards. Game over!")
            break

        # Evaluate the hand
        evaluation = evaluate_hand(hand)
        print(f"Hand evaluation: {evaluation}")

        # Payout for the hand
        payout = PAYOUTS[evaluation]
        money += payout
        print(f"You win ${payout}. Current money: ${money}")

        # Check if player wants to use the free redeal
        if not free_redeal_used:
            use_free_redeal = input("Would you like a free re-deal? (y/n): ").lower()
            if use_free_redeal == "y":
                free_redeal_used = True
                selected_indices = [int(i) for i in input("Enter indices of cards to replace (e.g., 0 2 4): ").split()]
                hand, deck = replace_selected_cards(hand, deck, selected_indices)
                print(f"Your new hand: {hand}")
                evaluation = evaluate_hand(hand)
                print(f"New hand evaluation: {evaluation}")
                payout = PAYOUTS[evaluation]
                money += payout
                print(f"You win ${payout}. Current money: ${money}")

        # Ask if the player wants to continue
        keep_playing = input("Do you want to keep playing? (y/n): ").lower()
        if keep_playing != "y":
            print(f"Game over! You finished with ${money}.")
            break

if __name__ == "__main__":
    main()
