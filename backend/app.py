from flask import Flask, jsonify, request
from flask_cors import CORS
from poker_logic import create_deck, shuffle_deck, deal_hand, replace_selected_cards, evaluate_hand

app = Flask(__name__)
CORS(app)

# Game state
deck = shuffle_deck(create_deck())  # Initialize the deck
hand = []  # Store the current hand globally
money = 100  # Starting money
free_redeal_used = False  # Free re-deal flag
payout_claimed = True  # Start as true to allow the first deal


@app.route('/api/deal', methods=['GET'])
def deal_cards():
    """
    Handles dealing a new hand.
    Deducts $10 and resets relevant game flags.
    """
    global deck, hand, money, free_redeal_used, payout_claimed

    if money < 10:
        return jsonify({"error": "Not enough money to deal cards."}), 400

    # Deduct cost for dealing cards
    money -= 10

    # Reshuffle the deck if needed
    if len(deck) < 5:
        deck[:] = shuffle_deck(create_deck())

    # Deal a new hand
    hand, deck[:] = deal_hand(deck)
    evaluation = evaluate_hand(hand)

    # Reset flags for the new hand
    free_redeal_used = False
    payout_claimed = False

    return jsonify({
        "hand": hand,
        "evaluation": evaluation,
        "money": money,
        "freeRedealAvailable": True
    })


@app.route('/api/redeal', methods=['POST'])
def redeal_cards():
    """
    Handles re-dealing selected cards.
    Allows one free re-deal per hand.
    """
    global deck, hand, free_redeal_used
    data = request.get_json()
    selected_indices = data.get("selectedCards", [])

    if free_redeal_used:
        return jsonify({"error": "Free re-deal has already been used."}), 400

    # Replace selected cards
    hand, deck[:] = replace_selected_cards(hand, deck, selected_indices)
    evaluation = evaluate_hand(hand)

    # Mark the free re-deal as used
    free_redeal_used = True

    return jsonify({
        "hand": hand,
        "evaluation": evaluation,
        "freeRedealAvailable": False
    })


@app.route('/api/payout', methods=['POST'])
def payout():
    """
    Handles calculating the payout based on the hand evaluation.
    Multiplies the bet amount by the hand multiplier.
    """
    global money, payout_claimed

    if payout_claimed:
        return jsonify({"error": "Payout has already been claimed."}), 400

    data = request.get_json()
    evaluation = data.get("evaluation", "")
    multipliers = {
        "Straight Flush!": 25,
        "Four of a Kind!": 15,
        "Full House!": 10,
        "Flush!": 5,
        "Straight!": 4,
        "Three of a Kind!": 3,
        "Two Pair!": 2,
        "Pair!": 1,
        "High Card!": 1,
        "Loss!": 0
    }

    if evaluation not in multipliers:
        return jsonify({"error": "Invalid evaluation for payout."}), 400
    
    multiplier = multipliers[evaluation]
    payout_amount = int(10 * multiplier)  # Based on $10 bet
    money += payout_amount
    payout_claimed = True

    return jsonify({"money": money, "payout": payout_amount})


if __name__ == '__main__':
    app.run(debug=True)
