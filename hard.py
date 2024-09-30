from ai_player import BattleshipAI

class HardAI(BattleshipAI):
    def __init__(self):
        super().__init__()
        self.targets = []

    '''def prep_targets(self, ships):
        """ Prepare a list of targets based on known ship positions """
        targets = []
        for ship in ships:
            targets.extend([(row, col) for row, col in ship])
        return targets'''

    def make_move(self, hit=False):
        """ Selects the next target from the queue of known ship positions """
        '''print("known targets..." + str(self.target_queue))
        if self.target_queue:
            target = self.target_queue.pop(0)  # Pop the first element to simulate systematic hitting
            self.shots.add(target)  # Add to shots to avoid hitting the same spot (if game rules allow revisits, this can be adjusted)
            print(f"Hitting {target}...")
            return target
        else:
            print("No more targets left.")
            return None'''
        print(f'targets: {self.targets}')
        row, col = self.targets[0][0], self.targets[0][1]
        self.targets.pop(0)
        return row, col
