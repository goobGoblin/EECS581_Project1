from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text
import time
# handles placing of player 1s ships
def placePlayer1Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    # timing from https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python
    # tracks time to place a ship
    startTime = time.time()
    # while the length of ships copy is greater than zero, we need to add ships
    while len(shipsCopy) > 0:
        # check on time
        currentTime = time.time()
        # if it is greater than 15 sec, exit the game
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        # if shipLength is greater than zero, we need to add ships
        if(shipLength > 0):
            # display that ship needs to be added
            stringofint = (str)(initialLength)
            toDisplay = 'Player 1, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            add_text.add_labels_ships(screen)
            add_text.add_labels_middle(screen)
            # get mouse position
            pos = pygame.mouse.get_pos()
            # print ship board for player 1
            battleship.printShipBoard(shipBoard, placedShips, [])
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the mouse was clicked, check that the ship placement is valid
                    # returns a 2 tuple with placedShips and a bool of if it was placed
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    # if it was placed, updaate start time and decrease ship length
                    if(wasPlaced):
                        startTime = time.time()
                        shipLength = shipLength - 1
            pygame.display.update()
        else:
            # if ship is placed, move on to the next ship
            shipsCopy.pop(0)
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1
# same as above but for player 2
def placePlayer2Ships(screen, ships, placedShips, shipBoard):
    shipsCopy = ships
    index = 0
    shipLength = shipsCopy[0]
    initialLength = shipLength
    startTime = time.time()
    while len(shipsCopy) > 0:
        currentTime = time.time()
        if currentTime - startTime > 15:
            add_text.time_out(screen)
            pygame.display.update()
            pause(3)
            pygame.quit()
            sys.exit()
        if(shipLength > 0):
            stringofint = (str)(initialLength)
            toDisplay = 'Player 2, place your ship of length ' + stringofint
            add_text.add_text(screen, toDisplay)
            pos = pygame.mouse.get_pos()
            battleship.printShipBoard(shipBoard, placedShips, [])
            # createPlayer1ShipGrid()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    attempt = addShip(shipBoard, placedShips, index, pos)
                    placedShips = attempt[0]
                    wasPlaced = attempt[1]
                    if(wasPlaced):
                        startTime = time.time()
                        shipLength = shipLength - 1
                   
            pygame.display.update()
        else:
            shipsCopy.pop(0)
            print(len(shipsCopy))
            if(len(shipsCopy) != 0):
                shipLength = shipsCopy[0]
                initialLength = shipLength
                index = index + 1


# handles logic for adding ship
def addShip(shipBoard, placedShips, index, pos):
    # starts at false
    shipAdded = False
    # gets the current ship
    currentShip = placedShips[index]
    # get rectangle that was selected
    rect = battleship.getRectangle(shipBoard, pos)
    # if row is invalid, make user click new spot
    if battleship.getRow(shipBoard, rect) == -1 or battleship.getCol(shipBoard, rect) == -1:
        return(placedShips, shipAdded) 
    # otherwise if it is a new ship make sure it is not already placed
    if(len(currentShip) == 0):
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
            shipAdded = True
    else:
        # if ship already exists, check that new addition isn't already placed and check that it touches the current ship
        alreadyPlaced = inShips(placedShips, pos)
        if not alreadyPlaced:
            touchesShipCheck = touchesShip(shipBoard, placedShips, index, pos)
            if touchesShipCheck:
                currentShip = addToShips(placedShips, pos, currentShip, shipBoard)
                shipAdded = True
    # add current ship to placedships
    placedShips[index] = currentShip
    # return placed ships and a bool of if it was added
    return (placedShips, shipAdded)

# checks that your placement touches the part of the ship already placed
def touchesShip(shipBoard, placedShips, index, pos):
    currentShip = placedShips[index]
    rect = battleship.getRectangle(shipBoard, pos)
    row = battleship.getRow(shipBoard, rect)
    col = battleship.getCol(shipBoard, rect)
    # if length is 1, it can be above, below, or either side
    if len(currentShip) == 1:
        for ship in currentShip:
            currentRow = battleship.getRow(shipBoard, ship)
            currentCol = battleship.getCol(shipBoard, ship)
            if row == currentRow:
                difference = abs(col-currentCol)
                if difference == 1:
                    return True
            elif col == currentCol:
                difference = abs(row-currentRow)
                if difference == 1:
                    return True
    else:
        # if length isn't one you need to check that it is aligned with currentship
        ship1 = currentShip[0]
        ship2 = currentShip[1]
        ship1row = battleship.getRow(shipBoard, ship1)
        ship2row = battleship.getRow(shipBoard, ship2)
        ship1col = battleship.getCol(shipBoard, ship1)
        ship2col = battleship.getCol(shipBoard, ship2)
        if ship1row == ship2row:
            for ship in currentShip:
                shiprow = battleship.getRow(shipBoard, ship)
                if row == shiprow:
                    shipcol = battleship.getCol(shipBoard, ship)
                    difference = abs(shipcol-col)
                    if difference == 1:
                        return True
        elif ship2col == ship1col:
            for ship in currentShip:
                shipcol = battleship.getCol(shipBoard, ship)
                if col == shipcol:
                    shiprow = battleship.getRow(shipBoard, ship)
                    difference = abs(shiprow-row)
                    if difference == 1:
                        return True
    return False



# checks if rect has already been placed
def inShips(placedShips, pos):
    for x in range(0, len(placedShips)):
        for y in range(0, len(placedShips[x])):
            tempRect = (placedShips[x])[y]
            if tempRect.collidepoint(pos):
                return True
    return False

# adds ship to current ship
def addToShips(placedShips, pos, currentShip, shipBoard):
    for x in range(0, 10):
        for y in range(0, 10):
            tempRect = (shipBoard[x])[y]
            if tempRect.collidepoint(pos):
                currentShip.append(tempRect)
                return currentShip
    return currentShip
    
