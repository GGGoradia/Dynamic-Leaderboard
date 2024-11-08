

class Leaderboard:
    def __init__(self):
        self.players = {}

    def update(self, name, score):
        score = int(score)
        if name in self.players:
            self.players[name] += score
        else:
            self.players[name] = score

    def get_leaderboard(self):
        sorted_leaderboard = sorted(self.players.items(), key=lambda item: item[1], reverse=True)
        return [{"name": name, "score": score} for name, score in sorted_leaderboard]
