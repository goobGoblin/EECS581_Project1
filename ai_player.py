import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
from abc import ABC, abstractmethod

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
            return False
        else:
            # otherwisecheck if you already hit the ship or already missed it, since you would need new user input
            tempRectShip = (shipBoard[row])[col]
            alreadyHit = battleship.inHits(hits, tempRectShip)
            alreadyMissed = battleship.inMisses(misses, tempRectShip)
            if alreadyHit or alreadyMissed: 
                return False

            hit = False
            tilesShot = battleship.tilesInShot(shipBoard, row, col, blastRadius)
            for row, col in tilesShot:
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
