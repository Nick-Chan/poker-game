from flask import Flask, jsonify
from flask_cors import CORS
from poker_logic import create_deck, shuffle_deck, deal_hand, evaluate_hand

app = Flask(__name__)

CORS(app)

# Initialize the deck
deck = shuffle_deck(create_deck())

@app.route('/api/deal', methods=['GET'])
def deal_cards():
    global deck
    hand, deck = deal_hand(deck)
    evaluation = evaluate_hand(hand)
    return jsonify({"hand": hand, "evaluation": evaluation})

if __name__ == '__main__':
    app.run(debug=True)
