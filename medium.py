from ai_player import BattleshipAI
import random

class MediumAI(BattleshipAI):
    def __init__(self):
        super().__init__()
        self.last_hit = None  # Track the coordinates of the last hit for targeted shooting

    def make_move(self, ship_hit):
        if ship_hit and self.last_hit:  # If the last move was a hit and there's a known last hit position
            print("Shooting orthogonally...")
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)  # Shuffle directions to vary attack pattern
            for d in directions:
                row, col = self.last_hit[0] + d[0], self.last_hit[1] + d[1]
                if 0 <= row < 10 and 0 <= col < 10 and (row, col) not in self.shots:
                    self.shots.add((row, col))
                    return row, col
            self.last_hit = None  # Reset last hit if no valid moves are available
        # Default to random shooting if not shooting orthogonally
        return self.random_shot()

    def random_shot(self):
        print("Shooting randomly...")
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self.shots:
                self.shots.add((row, col))
                return row, col

    def update_last_hit(self, row, col):
        self.last_hit = (row, col)
