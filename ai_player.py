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
