"""
Program Name: battleship.py

Description:
This program sets up and manages a Pygame-based Battleship game. It includes functions to create grids, manage hits, misses, and ship placements, as well as handling game turns and logic. The game has support for both single-player and multiplayer modes (with multiplayer being a future implementation).

Inputs:
- screen: The Pygame screen surface.
- pos: Mouse position for user clicks to determine ship placements and attacks.
- hits, misses: Arrays that track the hits and misses for each player.
- shipBoard, targetBoard: Grids representing the player's ships and attack targets.

Output:
- Displays and updates the game boards, showing ship placements, hits, misses, and game state (turns, sunk ships, etc.).

Code Sources:
- https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame (creating a grid in Pygame)
- https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame (handling mouse clicks on grid cells)
- Additional logic inspired by threads on creating a Snake game in Pygame.

Author: Zai Erb
Edited by: Harrison Reed
Creation Date: September 2, 2024
"""

import pygame

from typing import List, Tuple, Optional, Iterable

import add_text
import sys
import singleplayer
import multiplayer
# import get_game_mode
# import multiplayer

#colors in RGB form
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

GRID = List[List[pygame.Rect]]

#Initialize pygame, mixer, and load audio files
#####
pygame.init()
pygame.mixer.init()
BAUDIO = pygame.mixer.Sound("assets/waves.wav")
HAUDIO = pygame.mixer.Sound("assets/hit.mp3")
MAUDIO = pygame.mixer.Sound("assets/miss.mp3")
CAUDIO = pygame.mixer.Sound("assets/cannon.mp3")
BCHANNEL = pygame.mixer.Channel(0)
ACHANNEL = pygame.mixer.Channel(1)
BCHANNEL.play(BAUDIO, loops=-1)
windowInfo = pygame.display.Info()
WINDOW_HEIGHT = windowInfo.current_w#400
#width of window for pygame
WINDOW_WIDTH = windowInfo.current_h#600
SCREEN = pygame.display.set_mode((600,400), flags = pygame.SCALED) #Added scaling(Harrison), TODO add dynamic rezising 
# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# creates grid (10x10) with width and height of 20 for each block
def createPlayer1ShipGrid() -> GRID:
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(30, 230, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# creates grid (10x10) with width and height of 20 for each block
def createPlayer1TargetGrid() -> GRID:
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(260, 460, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard


player1ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it, represents player1board for their own ships
player1TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it, represents the targets for player 1
player1BlastRadius = 0
player1hits: List[pygame.Rect] =[] # will store rect objects of hits
player1misses: List[pygame.Rect]=[] # will store rect objects of misses
player1ships = [] # will hold the sizes for ships
player1placedShips: GRID = [[],[],[],[]]  # 2d array that will hold the placed ships for player 1
copyPlayer1placedShips = [] # non pointer copy of player1placedShips
# same as objects above but for player 2
player2ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
player2TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
player2BlastRadius = 0
player2hits: List[pygame.Rect] =[]
player2misses: List[pygame.Rect] =[]
player2ships = []
player2placedShips = [[],[],[],[]]
copyPlayer2placedShips = []
# keeps track of if it is player 1 turn
player1Turn = True
# track if ships have been placed
player1ready = False
player2ready = False
# track if game is over
gameover = False


def draw_menu_options(): 
    # used offset to move squares to center
    offset = 45
    # create rects for each choice
    rect1 = pygame.Rect(10+offset,200,50,50)
    rect2 = pygame.Rect(90+offset,200,50,50)
    rect3 = pygame.Rect(170+offset,200,50,50)
    rect4 = pygame.Rect(250+offset,200,50,50)
    # draw each rect
    pygame.draw.rect(SCREEN, WHITE, rect1, 1)
    pygame.draw.rect(SCREEN, WHITE, rect2, 1)
    pygame.draw.rect(SCREEN, WHITE, rect3, 1)
    pygame.draw.rect(SCREEN, WHITE, rect4, 1)
    # add text to boxes
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('1v1', True, RED)
    textRect = text.get_rect()
    textRect.center = (35+offset, 225)
    SCREEN.blit(text, textRect)
    text = font.render('Easy AI', True, RED)
    textRect = text.get_rect()
    textRect.center = (115+offset, 225)
    SCREEN.blit(text, textRect)
    text = font.render('Medium AI', True, RED)
    textRect = text.get_rect()
    textRect.center = (195+offset, 225)
    SCREEN.blit(text, textRect)
    text = font.render('Hard AI', True, RED)
    textRect = text.get_rect()
    textRect.center = (275+offset, 225)
    SCREEN.blit(text, textRect)


def main_menu(): 
    from get_ships_num import get_index
    option_chosen = False
    while not option_chosen: 
        draw_menu_options()
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # get the box that was selected and assign ships accordingly
                index = get_index(SCREEN, pos) 
                if index != -1: 
                    option_chosen = True
                    SCREEN.fill(BLACK, (0, 0, 490, 400))
                    if index == 1: 
                        multiplayer.run()
                    elif index == 2: 
                        singleplayer.run("easy")
                    elif index == 3: 
                        singleplayer.run("medium")
                    elif index == 4: 
                        singleplayer.run("hard")
        pygame.display.update()

# main handles all the logic and passing between files
def main():
    # following code is inspired and similar to thread on creating a grid for a snake game in pygane
    # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    global SCREEN, CLOCK
    # initializes pygame
    #pygame.init()
    # creates clock in pygame
    CLOCK = pygame.time.Clock()
    #fill screen to black
    #SCREEN.fill(BLACK)
    # to implement multiplayer game mode simply create a get_game_mode.py file that displays options for number of players and sets the mode based on what the user selects
    CLOCK.tick(60)
    main_menu()



# creates a shallow copy of a 2d array
def createShallowCopy(ships):
    temp = []
    temp2 = []
    for x in ships:
        temp2 = []
        for y in x:
            temp2.append(y)
        temp.append(temp2)
    return temp

# handles logic for user click
def checkForCollision(targetBoard: GRID, shipBoard: GRID, centerPos: Tuple[int, int], hits: List[pygame.Rect], misses: List[pygame.Rect], shipsPlaced: GRID, shipsCopy: GRID, blastRadius: int) -> bool:
    # get the rect object and row and col
    rect = getRectangle(targetBoard, centerPos)
    centerRow = getRow(targetBoard, rect)
    centerCol = getCol(targetBoard, rect)
    # if you have an invalid row, then you did not hit anything and need new user input
    if centerRow == -1 or centerCol == -1:
        return False
    else:
        # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
        tempRectShip = (shipBoard[centerRow])[centerCol]
        alreadyHit = inHits(hits, tempRectShip)
        alreadyMissed = inMisses(misses, tempRectShip)
        if alreadyHit or alreadyMissed: 
            return False
        
        hit = False
        tilesShot = tilesInShot(shipBoard, centerRow, centerCol, blastRadius)
        for row, col in tilesShot:
            inShipsList = inShips(shipsPlaced, shipBoard[row][col])
            if inShipsList:
                hit = True
                hits.append(targetBoard[row][col])
                hits.append(shipBoard[row][col])
                removeFromShipsCopy(shipBoard[row][col], shipsCopy)
            else:
                misses.append(targetBoard[row][col])
                misses.append(shipBoard[row][col])
        if hit: 
            pygame.time.delay(1500) 
            ACHANNEL.play(HAUDIO)
            add_text.add_text(SCREEN, 'You hit a ship!')
        else: 
            # otherwise you missed
            pygame.time.delay(1000) 
            ACHANNEL.play(MAUDIO) #Short delay to allow for a little bit of tension
            add_text.add_text(SCREEN, 'You did not hit a ship!')

    # return true since if you make it this far is was a valud move
    return True

def tilesInShot(grid: GRID, centerRow: int, centerCol: int, radius: int) -> List[Tuple[int, int]]:
    """
    Given a 2D array representation of a grid, returns a list of rows, columns for every grid item 
    <radius> distance away from <centerRow> and <centerCol>. Diagonals are a distance of 1 away. 
    """
    gridSize = len(grid)
    results = []
    
    # Define the possible bounds for the rows/cols in the shot
    minRow = centerRow - radius
    maxRow = centerRow + radius
    minCol = centerCol - radius
    maxCol = centerCol + radius

    for row in range(minRow,  maxRow + 1):
        for col in range(minCol, maxCol + 1):
            if 0 <= row < gridSize and 0 <= col < gridSize:
                results.append((row, col))
    
    return results


# removes rect from the copy so that you can track what ships have been hit    
def removeFromShipsCopy(rect: pygame.Rect, shipsCopy: GRID):
    for x in shipsCopy:
        for y in x:
            if rect == y:
                x.remove(y)

#checks if an array within 2-d array is empty. If so you have a sunk ship
def shipsSunk(shipsCopy) -> int:
    sunk = 0
    for x in shipsCopy:
        if(len(x) == 0):
            shipsCopy.remove(x)
            sunk += 1
    return sunk

# if shipsCopy has length 0 then all ships are sunk and game is over
def gameIsOver(shipsCopy) -> bool:
    if(len(shipsCopy) == 0):
        return True
    else:
        return False

# return rect object given the board and mouse position
# based off of https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame
def getRectangle(board: GRID, pos: Tuple[int, int]) -> Optional[pygame.Rect]:
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tempRect = (board[x])[y]
            if tempRect.collidepoint(pos):
                return tempRect

# return row of a rectangle
def getRow(board: GRID, rect: pygame.Rect) -> int:
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return x
    return -1

# return column of a rectangle
def getCol(board: GRID, rect: pygame.Rect) -> int:
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return y
    return -1

# check if a rectangle is in the hits array
def inHits(board: Iterable[pygame.Rect], rect: pygame.Rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the misses array
def inMisses(board: Iterable[pygame.Rect], rect: pygame.Rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the ships 2-d array
def inShips(board: GRID, rect: pygame.Rect):
    for x in board:
        for y in x:
            if rect == y:
                return True
    return False

# check if a rectangle is in the hit ships array
def inHitShips(hits: Iterable[pygame.Rect], rect: pygame.Rect):
    for x in hits:
        if rect == x:
            return True
    return False
    

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# prints a board given 2-d array created in above functions. checks for hits and misses and changes color accordingly
def printBoard(board: GRID, hits: Iterable[pygame.Rect], misses: Iterable[pygame.Rect]):
    for x in board:
        for y in x:
            if(inHits(hits, y)):
                pygame.draw.rect(SCREEN, RED, y, 1)
            elif(inMisses(misses, y)):
                pygame.draw.rect(SCREEN, GREEN, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# prints a board given 2-d array created in above functions. shows which of your ships have been hit
def printShipBoard(board: GRID, ships: GRID, hits: Iterable[pygame.Rect]):
    for x in board:
        for y in x:
            if(inShips(ships, y)):
                if(inHits(hits, y)):
                    pygame.draw.rect(SCREEN, RED, y, 1)
                else:
                    pygame.draw.rect(SCREEN, BLUE, y, 1)
            else:
                pygame.draw.rect(SCREEN, WHITE, y, 1)



# so that each import does not call main function
if __name__ == "__main__":
    main()
