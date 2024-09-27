import random
from ai_player import BattleshipAI

class MediumAI(BattleshipAI):
    def __init__(self):
        super().__init__()
        self.hits = []  # Stores coordinates of hits
        self.hunting_mode = False  # True if AI is in "hunt" mode
        self.last_hit = None  # Coordinates of the last hit
        self.directions = ['up', 'down', 'left', 'right']  # Directions to shoot after a hit
        self.current_direction = None  # Current direction AI is shooting in
        self.checked_directions = []  # Keep track of tried directions from a hit

    def make_move(self, target_board, ship_board, hits, misses):
        """
        The AI shoots randomly until a hit is found, then starts "hunting"
        in orthogonal directions to sink the ship.
        """
        if self.hunting_mode:
            return self.hunt_ship(target_board, ship_board, hits, misses)
        else:
            return self.random_shot(target_board, ship_board, hits, misses)

    def random_shot(self, target_board, ship_board, hits, misses):
        """
        Randomly selects an untried coordinate to fire at.
        Works with pygame.Rect objects.
        """
        print("AI shooting randomly...")
        while True:
            row = random.randint(0, len(target_board) - 1)
            col = random.randint(0, len(target_board[0]) - 1)
            
            # Get the rect object for the current row and col
            rect = target_board[row][col]
            
            # Check if the rect has already been hit or missed
            if rect not in hits and rect not in misses:
                self.shots.add((row, col))  # Record the shot for tracking
                
                # Check if it hits a ship (using ship_board to check for ships)
                if rect in ship_board[row]:
                    print(f"AI hit at ({row}, {col})")
                    self.hunting_mode = True
                    self.last_hit = (row, col)
                    self.checked_directions = []
                    hits.append(rect)  # Add the hit to the hits list
                else:
                    print(f"AI missed at ({row}, {col})")
                    misses.append(rect)  # Add the miss to the misses list
                    
                return row, col

    def hunt_ship(self, target_board, ship_board, hits, misses):
        """
        After getting a hit, this function fires in orthogonal directions (up, down, left, right)
        until the ship is sunk.
        """
        if not self.current_direction:
            self.current_direction = self.get_next_direction()

        row, col = self.get_next_hunt_position()

        # Get the rect object for the current row and col
        rect = target_board[row][col]

        # Check that the next position is within bounds and hasn't been fired at
        if (0 <= row < len(target_board)) and (0 <= col < len(target_board[0])) and rect not in self.shots:
            self.shots.add((row, col))
            if rect in ship_board[row]:
                print("AI hit at", row, col)
                self.last_hit = (row, col)  # Keep track of the last hit for continuous shooting
                hits.append(rect)  # Add to the hits list
            else:
                print("AI missed at", row, col)
                misses.append(rect)  # Add to the misses list
                # Switch direction if the current shot missed
                self.current_direction = self.get_next_direction()
            return row, col
        else:
            # If the next position is invalid or already shot, switch direction
            self.current_direction = self.get_next_direction()
            return self.hunt_ship(target_board, ship_board, hits, misses)

    def get_next_hunt_position(self):
        """
        Calculates the next position to shoot at based on the current direction.
        """
        row, col = self.last_hit
        if self.current_direction == 'up':
            return row - 1, col
        elif self.current_direction == 'down':
            return row + 1, col
        elif self.current_direction == 'left':
            return row, col - 1
        elif self.current_direction == 'right':
            return row, col + 1

    def get_next_direction(self):
        """
        Chooses the next direction to shoot in after a miss or when a direction is exhausted.
        """
        remaining_directions = [d for d in self.directions if d not in self.checked_directions]
        if remaining_directions:
            direction = random.choice(remaining_directions)
            self.checked_directions.append(direction)
            return direction
        else:
            # If all directions are exhausted, reset to random mode
            self.hunting_mode = False
            self.current_direction = None
            self.checked_directions = []
            return None
