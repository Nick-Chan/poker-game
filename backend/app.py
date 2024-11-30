from flask import Flask, jsonify, request
from flask_cors import CORS
from poker_logic import create_deck, shuffle_deck, deal_hand, replace_selected_cards, evaluate_hand

app = Flask(__name__)

CORS(app)

# Initialize the deck
deck = shuffle_deck(create_deck())

hand = []  # Store the current hand globally

@app.route('/api/deal', methods=['GET'])
def deal_cards():
    global deck, hand
    hand, deck = deal_hand(deck)
    evaluation = evaluate_hand(hand)
    return jsonify({"hand": hand, "evaluation": evaluation})

@app.route('/api/redeal', methods=['POST'])
def redeal_cards():
    global deck, hand
    data = request.get_json()
    selected_indices = data.get("selectedCards", [])

    hand, deck = replace_selected_cards(hand, deck, selected_indices)
    evaluation = evaluate_hand(hand)
    return jsonify({"hand": hand, "evaluation": evaluation})

if __name__ == '__main__':
    app.run(debug=True)