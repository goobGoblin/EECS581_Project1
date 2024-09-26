from abc import ABC, abstractmethod

class BattleshipAI(ABC):
    def __init__(self):
        self.ships = []
        self.shots = set()

    @abstractmethod
    def make_move(self):
        pass
