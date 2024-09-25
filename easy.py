from ai_player import BattleshipAI
import random

class EasyAI(BattleshipAI):
    def make_move(self):
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if (row, col) not in self.shots:
                self.shots.add((row, col))
                return row, col