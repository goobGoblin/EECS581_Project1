from ai_player import BattleshipAI
import random

class EasyAI(BattleshipAI):
    def make_move(self, hit=False):
        print(self.shots)
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self.shots:
                self.shots.add((row, col))
                return row, col
    
    