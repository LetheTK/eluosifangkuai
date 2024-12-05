import os
import json

class ScoreManager:
    def __init__(self):
        self.score_file = "highscore.json"
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            if os.path.exists(self.score_file):
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0

    def save_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            try:
                with open(self.score_file, 'w') as f:
                    json.dump({'high_score': score}, f)
            except:
                pass 