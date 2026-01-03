# server.py - Local leaderboard server (no external APIs)
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

LEADERBOARD_FILE = 'leaderboard.json'

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as f:
                data = json.load(f)
                return jsonify(data)
        else:
            return jsonify({"scores": []})
    except:
        return jsonify({"scores": []})

@app.route('/api/leaderboard', methods=['POST'])
def save_leaderboard():
    try:
        scores = request.json
        with open(LEADERBOARD_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)