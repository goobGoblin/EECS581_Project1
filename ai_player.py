import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
from abc import ABC, abstractmethod
import time
import random

class BattleshipAI(ABC):
    def __init__(self):
        self.ships = []
        self.shots = set()

    @abstractmethod
    def make_move(self):
        pass

    def checkForCollision(self, targetBoard, shipBoard, row, col, hits, misses, shipsPlaced, shipsCopy):
        pygame.time.delay(1000)
        print("checking for collision")
        hit = False 
        # if you have an invalid row, then you did not hit anything and need new user input
        if row == -1 or col == -1:
            return False
        else:
            # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
            tempRectTarget = (targetBoard[row])[col]
            tempRectShip = (shipBoard[row])[col]
            alreadyHit = battleship.inHits(hits, tempRectShip)
            alreadyMissed = battleship.inMisses(misses, tempRectShip)
            if alreadyHit or alreadyMissed: 
                return False
            # if it is in their ships, you have a hit
            inShipsList = battleship.inShips(shipsPlaced, tempRectShip)
            if inShipsList:
                battleship.ACHANNEL.play(battleship.HAUDIO)
                add_text.add_text(battleship.SCREEN, 'AI hit a ship!')
                pygame.time.delay(1500) 
                hits.append(tempRectTarget)
                hits.append(tempRectShip)
                battleship.removeFromShipsCopy(tempRectShip, shipsCopy)
            else:
                # otherwise you missed
                pygame.time.delay(1000) 
                battleship.ACHANNEL.play(battleship.MAUDIO) #Short delay to allow for a little bit of tension
                add_text.add_text(battleship.SCREEN, 'AI did not hit a ship!')
                misses.append(tempRectTarget)
                misses.append(tempRectShip)
        # return true since if you make it this far is was a valud move
        return True

    '''def placeShips(self, screen, ships, placedShips, shipBoard):
        shipsCopy = ships
        index = 0
        shipLength = shipsCopy[0]
        initialLength = shipLength
        startTime = time.time()
        while len(shipsCopy) > 0:
            print(f' len shipcopy: {len(shipsCopy)}')
            currentTime = time.time()
            if(shipLength > 0):
                x = random.randint(30, 230)
                y = random.randint(100, 300)
                pos = (x, y)
                battleship.printShipBoard(shipBoard, placedShips, [])
                print('placing ship')
                attempt = place_ships.addShip(shipBoard, placedShips, index, pos)
                placedShips = attempt[0]
                wasPlaced = attempt[1]
                if(wasPlaced):
                    print('ship placed')
                    if (x < 130):
                        for s in range(shipLength - 1):
                            x += 20
                            print(x)
                            pos = (x,y)
                            place_ships.addShip(shipBoard, placedShips, index, pos)
                            startTime = time.time()
                            shipLength = shipLength - 1
                            print(shipLength)
                    else:
                        for s in range(shipLength - 1):
                            x -= 20
                            pos = (x,y)
                            place_ships.addShip(shipBoard, placedShips, index, pos)
                            startTime = time.time()
                            shipLength = shipLength - 1
                pygame.display.update()
            else:
                shipsCopy.pop(0)
                print(len(shipsCopy))
                if(len(shipsCopy) != 0):
                    shipLength = shipsCopy[0]
                    initialLength = shipLength
                    index = index + 1'''
    def placeShips(self, screen, ships, placedShips, shipBoard):
        screen.fill((0, 0, 0))
        message = "Please wait while AI places ships"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        
        shipsCopy = ships
        print(shipsCopy)
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
                x = random.randint(30, 230)
                y = random.randint(100, 300)
                pos = (x, y)
                attempt = place_ships.addShip(shipBoard, placedShips, index, pos)
                placedShips = attempt[0]
                wasPlaced = attempt[1]
                if(wasPlaced):
                    rect = battleship.getRectangle(shipBoard, pos)
                    print(f'placed at column {battleship.getRow(shipBoard, rect) + 1}, row {battleship.getCol(shipBoard, rect) + 1}')
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
                    pygame.time.wait(2000)
        screen.fill((0, 0, 0))
                    
