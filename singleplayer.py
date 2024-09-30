"""
Program Name: singleplayer.py

Description:
This program contains the game loop and logic for running a multiplayer version of a Pygame-based Battleship game. It handles the placement of ships for both Player 1 and Player 2, manages turns, updates the game board with hits and misses, and determines when the game is over. The game operates in two-player mode, alternating between the players until one player wins by sinking all of the opponent's ships.

Inputs:
- pos: Mouse position for determining player actions on the grid.
- player1ships, player2ships: Arrays containing the lengths of the ships for Player 1 and Player 2.
- player1placedShips, player2placedShips: 2D arrays representing the positions of the ships for both players.
- player1hits, player2hits: Arrays tracking the hits made by each player.
- player1misses, player2misses: Arrays tracking the misses made by each player.

Output:
- Displays updates to the game board, including ship placements, hits, misses, and win/loss messages.
- Alternates between Player 1 and Player 2 turns, showing the appropriate updates after each move.

Code Sources:
- Pygame documentation for event handling and drawing.
- Based on previously implemented grid and logic for Battleship game in Pygame.

Author: Zai Erb

Creation Date: September 2, 2024
"""


from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
# import get_game_mode

def run():

    # this is the code for multiplayer I haven't written anything for singleplayer yet
    print("singleplayer")
    # get the number of ships that the user wants for the game and returns a 4 tupe with size and empty placed ships array
    arrays = get_ships_num.get_ships(battleship.player1ships, battleship.player2ships, battleship.SCREEN, battleship.player1placedShips, battleship.player2placedShips)
    battleship.player1ships = arrays[0]
    battleship.player2ships = arrays[1]
    battleship.player1placedShips = arrays[2]
    battleship.player2placedShips = arrays[3]
    clock = pygame.time.Clock()
    #run while the game is not ended
    while not battleship.gameover:
        
        # gets the position of the mouse on the screen
        pos = pygame.mouse.get_pos()
        
        #########################################################
        
        # if player 1 is not ready, pass to place_ships and have player 1 place their ships
        if not battleship.player1ready:
            place_ships.placePlayer1Ships(battleship.SCREEN, battleship.player1ships, battleship.player1placedShips, battleship.player1ShipBoard)
            battleship.player1ready = True
            #create non pointer copy
            battleship.copyPlayer1placedShips = battleship.createShallowCopy(battleship.player1placedShips)  
        # repeat for player 2
        if not battleship.player2ready:
            place_ships.placePlayer2Ships(battleship.SCREEN, battleship.player2ships, battleship.player2placedShips, battleship.player2ShipBoard)
            battleship.player2ready = True
            battleship.copyPlayer2placedShips = battleship.createShallowCopy(battleship.player2placedShips)  
        # add text saying battleship and add rows and cols
        add_text.add_text(battleship.SCREEN, 'Battleship')
        add_text.add_labels_targets(battleship.SCREEN)
        # if it is player 1 turn, say that and print their boards
        if(battleship.player1Turn):
            add_text.add_text(battleship.SCREEN, 'Player 1 Turn')
            battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
            battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)
        # if it is player 2 turn, say that and print their boards
        else:
            add_text.add_text(battleship.SCREEN, 'Player 2 Turn')
            battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits)
            battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)
        # handles events in pygame
            # if the user wants to quit, close pygame
            # if the user clicks, we respond accordingly
        keys = pygame.key.get_pressed()
        event = pygame.event.poll() #got rid of loop since the events are stored on a queue, and was consuming 
                                    #input when not wanted
        #########################################################
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                pygame.mixer.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
         # if it is player 1 turn, check for a hit and checkForCollision will handle all the logic for updating hits and misses
            
            if(battleship.player1Turn):
                battleship.ACHANNEL.play(battleship.CAUDIO) #sound effect for firing cannon
                pygame.time.delay(1000) #Short delay to allow for a little bit of tension
                played = battleship.checkForCollision(battleship.player1TargetBoard, battleship.player2ShipBoard, pos, battleship.player1hits, battleship.player1misses, battleship.player2placedShips, battleship.copyPlayer2placedShips, battleship.player1BlastRadius)
                if played: 
                    # if they made a valid move, update the boards
                    battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
                    battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
                    add_text.add_labels_middle(battleship.SCREEN)
                    add_text.add_labels_ships(battleship.SCREEN)
                    pygame.display.update()
                    # check for a sunk ship
                    shipsSunk = battleship.shipsSunk(battleship.copyPlayer2placedShips)
                    # if they sunk a ship, check if all ships are sunk
                    if(shipsSunk > 0):
                        battleship.player1BlastRadius += shipsSunk
                        add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                        pygame.display.update()
                        ended = battleship.gameIsOver(battleship.copyPlayer2placedShips)
                        if ended:
                            battleship.gameover = True
                            add_text.add_text(battleship.SCREEN, 'Player 1 won!')
                            pygame.display.update()
                            pygame.time.wait(2000)#Let the game sit for a little before closing
                            add_text.ask_play_again(battleship.SCREEN)
                        # wait for 1 seconds and switch turn
                    pause(1)
                    if not battleship.gameover:
                        add_text.add_black_screen(battleship.SCREEN)
                        pygame.display.update()
                        pygame.time.wait(2000)#Updated to fix bug where game still accepts input during black screen(The loop)
                        pygame.event.clear()#clear the queue to avoid input during black screen
                    battleship.player1Turn = False
            else:
                    # otherwise repeat for player 2
                battleship.ACHANNEL.play(battleship.CAUDIO) #sound effect for firing cannon
                played = battleship.checkForCollision(battleship.player2TargetBoard, battleship.player1ShipBoard, pos, battleship.player2hits, battleship.player2misses, battleship.player1placedShips, battleship.copyPlayer1placedShips, battleship.player2BlastRadius)
                pygame.time.delay(1000) #Short delay to allow for a little bit of tension
                if played:
                    battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits)
                    battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
                    add_text.add_labels_middle(battleship.SCREEN)
                    add_text.add_labels_ships(battleship.SCREEN)
                    pygame.display.update()
                    shipsSunk = battleship.shipsSunk(battleship.copyPlayer1placedShips)
                    if(shipsSunk > 0):
                        battleship.player2BlastRadius += shipsSunk
                        add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                        pygame.display.update()
                        ended = battleship.gameIsOver(battleship.copyPlayer1placedShips)
                        if ended:
                            battleship.gameover = True
                            add_text.add_text(battleship.SCREEN, 'Player 2 won!')
                            pygame.display.update()
                            pygame.time.wait(2000) #Let the game sit for a little before closing
                            add_text.ask_play_again(battleship.SCREEN)
                    pause(1)
                    if not battleship.gameover:
                        add_text.add_black_screen(battleship.SCREEN)
                        pygame.display.update()
                        pygame.time.wait(2000) #Updated to fix bug where game still accepts input during black screen(The loop)
                        pygame.event.clear() #Clear the queue to avoid input during black screen
                        
                    battleship.player1Turn = True
        
        pygame.display.update()
    
    print("Out of loop")
    
    #See if the user wants to play again
    #add_text.ask_play_again(battleship.SCREEN)

    while True:
        for event in pygame.event.get():
            print("In loop")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    print ("yes")
                    battleship.gameover = False
                    battleship.player1Turn = True
                    battleship.player1ready = False
                    battleship.player2ready = False
                    battleship.player1hits = []
                    battleship.player1misses = []
                    battleship.player1BlastRadius = 0
                    battleship.player2hits = []
                    battleship.player2misses = []
                    battleship.player1placedShips = []
                    battleship.player2placedShips = []
                    battleship.player1ships = []
                    battleship.player2ships = []
                    battleship.player2BlastRadius = 0
                    battleship.SCREEN.fill((0,0,0))
                    pygame.display.update()
                    run()
                    break
                elif(event.key == pygame.K_n):
                    pygame.quit()
                    sys.exit()
                    break

        
