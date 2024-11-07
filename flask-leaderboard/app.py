from flask import Flask, request, jsonify
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

class Leaderboard:
    def __init__(self):
        self.players = {}

    def add_player(self, name, score):
        score = int(score)
        if name in self.players:
            self.players[name] += score
        else:
            self.players[name] = score

    def get_leaderboard(self):
        sorted_leaderboard = sorted(self.players.items(), key=lambda item: item[1], reverse=True)
        return [{"name": name, "score": score} for name, score in sorted_leaderboard]

leaderboard = Leaderboard()
clients = []

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard_data = leaderboard.get_leaderboard()
    return jsonify(leaderboard_data)

@app.route('/api/update', methods=['POST'])
def update_leaderboard():
    player_data = request.get_json()
    leaderboard.add_player(player_data['name'], player_data['score'])

    # Broadcast the updated leaderboard to all WebSocket clients
    leaderboard_data = json.dumps(leaderboard.get_leaderboard())
    for ws in clients[:]:
        try:
            ws.send(leaderboard_data)
        except Exception as e:
            print("Error sending to client:", e)
            clients.remove(ws)  # Remove disconnected clients

    return jsonify({'message': 'Leaderboard updated successfully!'})

@sock.route('/ws/leaderboard')
def leaderboard_ws(ws):
    # Add the WebSocket connection to the clients list
    clients.append(ws)
    try:
        # Send the current leaderboard data upon connection
        ws.send(json.dumps(leaderboard.get_leaderboard()))
        
        # Keep the connection open to listen for incoming messages or disconnection
        while True:
            message = ws.receive()
            if message is None:
                break  # Exit if the client disconnects
    finally:
        # Remove the client from the list upon disconnection
        clients.remove(ws)

if __name__ == "__main__":
    app.run(debug=True)
