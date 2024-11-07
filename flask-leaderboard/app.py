from flask import Flask, render_template, request, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

class Leaderboard:
    def __init__(self):
        self.players = {}  # Dictionary to store player names and scores

    def add_player(self, name, score):
        # Convert score to an integer to avoid concatenation
        score = int(score)
        # Add to existing score if player exists; otherwise, add new player
        if name in self.players:
            self.players[name] += score
        else:
            self.players[name] = score

    def get_leaderboard(self):
        # Sort players by score in descending order and return as a list of dictionaries
        sorted_leaderboard = sorted(self.players.items(), key=lambda item: item[1], reverse=True)
        return [{"name": name, "score": score} for name, score in sorted_leaderboard]

# Initialize the leaderboard
leaderboard = Leaderboard()

# Store connected WebSocket clients
clients = []

# Function to read the Peerfile and create a list of addresses
def read_peerfile():
    try:
        with open('Peerfile', 'r') as file:
            peer_addresses = [line.strip() for line in file if line.strip()]
        return peer_addresses
    except FileNotFoundError:
        print("Peerfile not found.")
        return []

# Load peer addresses on startup
peer_list = read_peerfile()

@app.route('/')
def index():
    return render_template('leaderboard.html')

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # Fetch leaderboard data
    leaderboard_data = leaderboard.get_leaderboard()
    return jsonify(leaderboard_data)

@app.route('/api/update', methods=['POST'])
def update_leaderboard():
    # Update leaderboard with new player data
    player_data = request.get_json()
    leaderboard.add_player(player_data['name'], player_data['score'])
    
    # Broadcast the updated leaderboard to all WebSocket clients
    leaderboard_data = json.dumps(leaderboard.get_leaderboard())
    for ws in clients:
        ws.send(leaderboard_data)
    
    return jsonify({'message': 'Leaderboard updated successfully!'})

# WebSocket route for real-time leaderboard updates
@sock.route('/ws/leaderboard')
def leaderboard_ws(ws):
    # Add the new WebSocket connection to the clients list
    clients.append(ws)
    
    # Send the initial leaderboard data on connection
    ws.send(json.dumps(leaderboard.get_leaderboard()))

    # Listen for client disconnection
    while True:
        if ws.closed:
            clients.remove(ws)
            break

# Optional: Add an endpoint to retrieve peer addresses if needed
@app.route('/api/peers', methods=['GET'])
def get_peers():
    return jsonify(peer_list)

if __name__ == '__main__':
    app.run(debug=True)
