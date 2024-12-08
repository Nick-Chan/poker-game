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

@app.route('/api/deal', methods=['GET'])
def deal_cards():
    global deck, hand, money, free_redeal_used
    if money < 10:
        return jsonify({"error": "Not enough money to deal cards."}), 400

    # Deduct cost for dealing cards
    money -= 10

    # Deal a hand and reset the free re-deal flag
    if len(deck) < 5:  # Reshuffle if not enough cards
        deck[:] = shuffle_deck(create_deck())
        free_redeal_used = False

    hand, deck[:] = deal_hand(deck)
    evaluation = evaluate_hand(hand)

    return jsonify({
        "hand": hand,
        "evaluation": evaluation,
        "money": money,
        "freeRedealAvailable": not free_redeal_used
    })

@app.route('/api/redeal', methods=['POST'])
def redeal_cards():
    global deck, hand, money, free_redeal_used
    data = request.get_json()
    selected_indices = data.get("selectedCards", [])

    if free_redeal_used:
        return jsonify({"error": "Free re-deal has already been used."}), 400

    # Redeal selected cards
    hand, deck[:] = replace_selected_cards(hand, deck, selected_indices)
    evaluation = evaluate_hand(hand)

    # Mark the free re-deal as used
    free_redeal_used = True

    return jsonify({
        "hand": hand,
        "evaluation": evaluation,
        "money": money,
        "freeRedealAvailable": not free_redeal_used
    })

@app.route('/api/payout', methods=['POST'])
def payout():
    global money
    data = request.get_json()
    evaluation = data.get("evaluation", "")
    payouts = {
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
    payout_amount = payouts.get(evaluation, 0)
    money += payout_amount
    return jsonify({"money": money, "payout": payout_amount})

if __name__ == '__main__':
    app.run(debug=True)
