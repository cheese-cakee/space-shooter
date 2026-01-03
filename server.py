# server.py
from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GIST_ID = "dbbb7b95e20b9119cd4ece2664932aaa"
API_TOKEN = os.environ.get('GITHUB_TOKEN')

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        url = f"https://api.github.com/gists/{GIST_ID}"
        response = requests.get(url, timeout=5)
        content = response.json()['files']['space-shooter-scores.json']['content']
        return jsonify(json.loads(content))
    except:
        return jsonify({"scores": []})

@app.route('/api/leaderboard', methods=['POST'])
def save_leaderboard():
    if not API_TOKEN:
        return jsonify({"error": "No GitHub token configured"}), 500
    
    try:
        scores = request.json
        url = f"https://api.github.com/gists/{GIST_ID}"
        data = {"files": {"space-shooter-scores.json": {"content": json.dumps(scores)}}}
        
        headers = {
            "Authorization": f"token {API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.patch(url, json=data, headers=headers, timeout=5)
        response.raise_for_status()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)