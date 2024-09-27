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

    def print_board_debug(self, target_board, ship_board, hits, misses):
        """
        Debugging method to print the current state of the board, including ships.
        """
        print("\n--- Target Board Status (S = Ship, H = Hit, M = Miss) ---")
        for row in range(len(target_board)):
            row_status = ""
            for col in range(len(target_board[0])):
                rect = target_board[row][col]
                if rect in hits:
                    row_status += " H "  # Hit
                elif rect in misses:
                    row_status += " M "  # Miss
                elif rect in ship_board[row]:
                    row_status += " S "  # Ship
                else:
                    row_status += " . "  # Untouched
            print(row_status)
        print("\n")

    def make_move(self, target_board, ship_board, hits, misses):
        """
        The AI shoots randomly until a hit is found, then starts "hunting"
        in orthogonal directions to sink the ship.
        """
        print("Current Mode: Hunting" if self.hunting_mode else "Current Mode: Random")
        self.print_board_debug(target_board, ship_board, hits, misses)

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
                print(f"AI shooting at ({row}, {col})")
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
            print(f"AI hunting at ({row}, {col}) in direction {self.current_direction}")
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
            print(f"AI switching direction from {self.current_direction}")
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
            print(f"AI switching to direction {direction}")
            return direction
        else:
            # If all directions are exhausted, reset to random mode
            print("All directions exhausted, switching to random mode")
            self.hunting_mode = False
            self.current_direction = None
            self.checked_directions = []
            return None
