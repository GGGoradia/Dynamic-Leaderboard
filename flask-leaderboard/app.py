from flask import Flask, render_template, request, jsonify
from leaderboard import Leaderboard

app = Flask(__name__)

# Initialize the leaderboard with a binary tree structure
leaderboard = Leaderboard()

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

if __name__ == '__main__':
    app.run(debug=True)
