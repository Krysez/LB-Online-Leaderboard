from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, template_folder="templates")

def load_contributions():
    try:
        with open("contributions.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route("/leaderboard")
def leaderboard():
    data = load_contributions()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return render_template("leaderboard.html", leaderboard=sorted_data)

@app.route("/api/leaderboard")
def api_leaderboard():
    data = load_contributions()
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_data)
