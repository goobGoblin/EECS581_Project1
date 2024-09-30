import pygame
import sys
import add_text
import place_ships
import battleship
from abc import ABC, abstractmethod
from matplotlib.pyplot import pause
import time
import random

class BattleshipAI(ABC):
    def __init__(self):
        self.ships = []
        self.shots = set()

    @abstractmethod
    def make_move(self):
        pass

    def checkForCollision(self, targetBoard, shipBoard, row, col, hits, misses, shipsPlaced, shipsCopy, blastRadius):
        pygame.time.delay(1000)
        print("checking for collision")
        # if you have an invalid row, then you did not hit anything and need new user input
        if row == -1 or col == -1:
            print('row -1 block')
            return False
        else:
            # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
            tempRectShip = (shipBoard[row])[col]
            alreadyHit = battleship.inHits(hits, tempRectShip)
            alreadyMissed = battleship.inMisses(misses, tempRectShip)
            if alreadyHit or alreadyMissed: 
                print('already hit block')
                return False

            hit = False
            tilesShot = battleship.tilesInShot(shipBoard, row, col, blastRadius)
            for row, col in tilesShot:
                print(f'Row and col: {row}, {col}')
                self.shots.add((row, col))
                inShipsList = battleship.inShips(shipsPlaced, shipBoard[row][col])
                if inShipsList:
                    hit = True
                    hits.append(targetBoard[row][col])
                    hits.append(shipBoard[row][col])
                    battleship.removeFromShipsCopy(shipBoard[row][col], shipsCopy)
                else:
                    misses.append(targetBoard[row][col])
                    misses.append(shipBoard[row][col])
            if hit: 
                pygame.time.delay(1500) 
                add_text.add_text(battleship.SCREEN, 'AI hit a ship!')
            else: 
                # otherwise you missed
                pygame.time.delay(1000) 
                add_text.add_text(battleship.SCREEN, 'AI did not hit a ship!')

        # return true since if you make it this far is was a valud move
        return True

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
                    
