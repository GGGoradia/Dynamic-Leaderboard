from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    return jsonify({'message': 'Leaderboard updated successfully!'})

# Optional: Add an endpoint to retrieve peer addresses if needed
@app.route('/api/peers', methods=['GET'])
def get_peers():
    return jsonify(peer_list)

if __name__ == '__main__':
    app.run(debug=True)
