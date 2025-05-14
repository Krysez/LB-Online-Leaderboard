from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime

app = Flask(__name__, template_folder="templates")

CONTRIB_FILE = "contributions.json"
SEASON_FILE = "season.json"

def load_contributions():
    try:
        with open(CONTRIB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_contributions(data):
    with open(CONTRIB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_seasons():
    try:
        with open(SEASON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_seasons(seasons):
    with open(SEASON_FILE, "w") as f:
        json.dump(seasons, f, indent=2)

@app.route("/leaderboard")
def leaderboard():
    data = load_contributions()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    seasons = load_seasons()
    return render_template("leaderboard.html", leaderboard=sorted_data, seasons=seasons[-3:][::-1])

@app.route("/api/leaderboard")
def api_leaderboard():
    data = load_contributions()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_data)

@app.route("/sync", methods=["POST"])
def sync():
    data = request.json
    if not isinstance(data, dict):
        return "Invalid format", 400
    save_contributions(data)
    return "Synced", 200

@app.route("/reset", methods=["POST"])
def reset():
    current = load_contributions()
    if not current:
        return "Nothing to archive", 204

    sorted_data = sorted(current.items(), key=lambda x: x[1], reverse=True)[:3]
    now = datetime.utcnow()
    date_str = now.strftime("%B %Y")

    seasons = load_seasons()
    new_season = {
        "season": len(seasons) + 1,
        "date": date_str,
        "top": sorted_data
    }

    seasons.append(new_season)
    save_seasons(seasons)
    save_contributions({})
    return "Leaderboard reset and archived", 200
