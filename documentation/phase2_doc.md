# Project Documentation: Battleship Game

## Overview
This project is a Python-based implementation of the classic game "Battleship", developed using Pygame. It features single-player mode against an AI opponent with plans for future implementation of multiplayer mode.

## Files and Directories

### `battleship.py`
- **Description**: Main game engine. Initializes the game, manages game states, and handles rendering and the main game loop.
- **Main Functions**:
  - `main()`: Initializes the game environment, calls setup functions, and contains the main game loop.
  - `checkForCollision()`: Checks if a shot hits or misses and updates game state accordingly.

### `singleplayer.py`
- **Description**: Manages the single-player gameplay logic, interfacing with the AI and managing user interactions.
- **Main Functions**:
  - `run()`: Main loop for single-player mode, handling player turns, AI moves, and game progression.

### `ai_player.py`
- **Description**: Abstract base class for AI players.
- **Classes**:
  - `BattleshipAI`: Base class defining the structure and functionalities for AI players.

### `medium.py`
- **Description**: Implements Medium difficulty AI logic.
- **Classes**:
  - `MediumAI`: Extends `BattleshipAI` with specific strategies for medium difficulty.

### `easy.py`
- **Description**: Implements Easy difficulty AI logic.
- **Classes**:
  - `EasyAI`: Implements a basic random shooting strategy for AI.

### `place_ships.py`
- **Description**: Contains functions to place ships on the game board at the start of the game.
- **Functions**:
  - `placePlayer1Ships()`: Places Player 1's ships.
  - `placePlayer2Ships()`: Places Player 2's ships (AI in single-player).

### `add_text.py`
- **Description**: Utility functions to add text and labels to the game screen.
- **Functions**:
  - `add_text()`: Displays text on the game screen.

### `get_ships_num.py`
- **Description**: Functions to get the number of ships for each player at the start of the game.
- **Functions**:
  - `get_ships()`: Initializes the ship count and placement for each player.

## Game Flow

1. **Initialization**: Sets up Pygame, loads resources, and initializes game states.
2. **Ship Placement**: Players place their ships on their respective grids.
3. **Game Loop**: Alternates turns between the player and AI, each attempting to hit the opponent's ships.
4. **End Game**: The game concludes when all ships of a player are sunk. Offers a replay option.

## Additional Notes

- The game is currently in the development phase, with features like multiplayer still to be implemented.
- AI strategies vary between levels, with Easy using randomized logic and Medium employing a more sophisticated, reactive approach based on hits.