import pygame
import os
import asyncio
from os.path import join
from random import randint, uniform
import json
import requests

# GitHub Gist configuration
GIST_ID = "dbbb7b95e20b9119cd4ece2664932aaa" 
API_TOKEN = os.environ.get('GITHUB_TOKEN', '')  # Set GITHUB_TOKEN in environment variables

def load_leaderboard():
    try:
        # Try local file first
        if os.path.exists('leaderboard.json'):
            with open('leaderboard.json', 'r') as f:
                return json.load(f)
        
        # Fallback to empty leaderboard
        return {"scores": []}
    except:
        return {"scores": []}

def save_score_locally(name, score):
    try:
        data = load_leaderboard()
        data["scores"].append({"name": name, "score": score})
        data["scores"].sort(key=lambda x: x["score"], reverse=True)
        data["scores"] = data["scores"][:10]  # Keep top 10
        
        with open('leaderboard.json', 'w') as f:
            json.dump(data, f)
    except:
        pass

# Rest of your existing game code...
# (Copy the rest of your original main.py here, but without any hardcoded secrets)