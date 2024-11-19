from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/deal', methods=['GET'])
def deal():
    return jsonify({"message": "Dealing cards!"})

if __name__ == '__main__':
    app.run(debug=True)
