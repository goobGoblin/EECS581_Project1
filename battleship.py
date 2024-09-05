import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import singleplayer
# import get_game_mode
# import multiplayer

#colors in RGB form
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
# height of window for pygame
WINDOW_HEIGHT = 400
#width of window for pygame
WINDOW_WIDTH = 490
#initializes screen in pygame
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# creates grid (10x10) with width and height of 20 for each block
def createPlayer1ShipGrid():
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
def createPlayer1TargetGrid():
    blockSize = 20 #Set the size of the grid block
    playerBoard = []
    for x in range(260, WINDOW_WIDTH-30, blockSize):
        subBoard = []
        for y in range(100, 300, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            subBoard.append(rect)
            #pygame.draw.rect(SCREEN, WHITE, rect, 1)
        playerBoard.append(subBoard)
    return playerBoard


player1ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it, represents player1board for their own ships
player1TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it, represents the targets for player 1
player1hits=[] # will store rect objects of hits
player1misses=[] # will store rect objects of misses
player1ships = [] # will hold the sizes for ships
player1placedShips = [[],[],[],[]]  # 2d array that will hold the placed ships for player 1
copyPlayer1placedShips = [] # non pointer copy of player1placedShips
# same as objects above but for player 2
player2ShipBoard = createPlayer1ShipGrid() # 2-D array with rects stored in it
player2TargetBoard = createPlayer1TargetGrid() # 2-D array with rects stored in it
player2hits=[]
player2misses=[]
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


# main handles all the logic and passing between files
def main():
    # following code is inspired and similar to thread on creating a grid for a snake game in pygane
    # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    global SCREEN, CLOCK
    # initializes pygame
    pygame.init()
    # creates clock in pygame
    CLOCK = pygame.time.Clock()
    #fill screen to black
    SCREEN.fill(BLACK)
    # to implement multiplayer game mode simply create a get_game_mode.py file that displays options for number of players and sets the mode based on what the user selects
    isSingleplayer = 1; #get_game_mode.set_mode(SCREEN) - FOR MULTIPLAYER IMPLEMENTATION
    if(isSingleplayer):
        singleplayer.run()
    # else:
        # multiplayer.run()


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
def checkForCollision(targetBoard, shipBoard, pos, hits, misses, shipsPlaced, shipsCopy):
    hit = False 
    # get the rect object and row and col
    rect = getRectangle(targetBoard, pos)
    row = getRow(targetBoard, rect)
    col = getCol(targetBoard, rect)
    # if you have an invalid row, then you did not hit anything and need new user input
    if row == -1 or col == -1:
        return False
    else:
        # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
        tempRectTarget = (targetBoard[row])[col]
        tempRectShip = (shipBoard[row])[col]
        alreadyHit = inHits(hits, tempRectShip)
        alreadyMissed = inMisses(misses, tempRectShip)
        if alreadyHit or alreadyMissed: 
            return False
        # if it is in their ships, you have a hit
        inShipsList = inShips(shipsPlaced, tempRectShip)
        if inShipsList:
            add_text.add_text(SCREEN, 'You hit a ship!')
            hits.append(tempRectTarget)
            hits.append(tempRectShip)
            removeFromShipsCopy(tempRectShip, shipsCopy)
        else:
            # otherwise you missed
            add_text.add_text(SCREEN, 'You did not hit a ship!')
            misses.append(tempRectTarget)
            misses.append(tempRectShip)
    # return true since if you make it this far is was a valud move
    return True

# removes rect from the copy so that you can track what ships have been hit    
def removeFromShipsCopy(rect, shipsCopy):
    for x in shipsCopy:
        for y in x:
            if rect == y:
                x.remove(y)

#checks if an array within 2-d array is empty. If so you have a sunk ship
def shipSunk(shipsCopy):
    for x in shipsCopy:
        if(len(x) == 0):
            shipsCopy.remove(x)
            return True
    return False

# if shipsCopy has length 0 then all ships are sunk and game is over
def gameIsOver(shipsCopy):
    if(len(shipsCopy) == 0):
        return True
    else:
        return False

# return rect object given the board and mouse position
# based off of https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame
def getRectangle(board, pos):
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tempRect = (board[x])[y]
            if tempRect.collidepoint(pos):
                return tempRect

# return row of a rectangle
def getRow(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return x
    #print(tempRect)
    return -1

# return column of a rectangle
def getCol(board, rect):
    tempRect = None
    for x in range(0, 10):
        for y in range(0,10):
            tempRect = (board[x])[y]
            if tempRect == rect:
                return y
    #print(tempRect)
    return -1

# check if a rectangle is in the hits array
def inHits(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the misses array
def inMisses(board, rect):
    for x in board:
        if rect == x:
            return True
    return False

# check if a rectangle is in the ships 2-d array
def inShips(board, rect):
    for x in board:
        for y in x:
            if rect == y:
                return True
    return False

# check if a rectangle is in the hit ships array
def inHitShips(hits, rect):
    for x in hits:
        if rect == x:
            return True
    return False

# following code is inspired and similar to thread on creating a grid for a snake game in pygane
# https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
# prints a board given 2-d array created in above functions. checks for hits and misses and changes color accordingly
def printBoard(board, hits, misses):
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
def printShipBoard(board, ships, hits):
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
