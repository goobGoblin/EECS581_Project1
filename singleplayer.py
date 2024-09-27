import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
from medium import MediumAI  # Import the medium AI

def run():
    print("singleplayer")

    # Initialize Medium AI for Player 2
    ai = MediumAI()

    # get the number of ships that the user wants for the game and returns a 4 tuple with size and empty placed ships array
    arrays = get_ships_num.get_ships(battleship.player1ships, battleship.player2ships, battleship.SCREEN, battleship.player1placedShips, battleship.player2placedShips)
    battleship.player1ships = arrays[0]
    battleship.player2ships = arrays[1]
    battleship.player1placedShips = arrays[2]
    battleship.player2placedShips = arrays[3]
    clock = pygame.time.Clock()

    # Run while the game is not ended
    while not battleship.gameover:
        pos = pygame.mouse.get_pos()

        # Player 1 places their ships
        if not battleship.player1ready:
            place_ships.placePlayer1Ships(battleship.SCREEN, battleship.player1ships, battleship.player1placedShips, battleship.player1ShipBoard)
            battleship.player1ready = True
            battleship.copyPlayer1placedShips = battleship.createShallowCopy(battleship.player1placedShips)

        # Player 2 (AI) places ships
        if not battleship.player2ready:
            place_ships.placePlayer2Ships(battleship.SCREEN, battleship.player2ships, battleship.player2placedShips, battleship.player2ShipBoard)
            battleship.player2ready = True
            battleship.copyPlayer2placedShips = battleship.createShallowCopy(battleship.player2placedShips)

        add_text.add_text(battleship.SCREEN, 'Battleship')
        add_text.add_labels_targets(battleship.SCREEN)

        # Player 1's turn
        if battleship.player1Turn:
            add_text.add_text(battleship.SCREEN, 'Player 1 Turn')
            battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
            battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)

        # Player 2's turn (AI)
        else:
            add_text.add_text(battleship.SCREEN, 'Player 2 (AI) Turn')
            battleship.printShipBoard(battleship.player2ShipBoard, battleship.player2placedShips, battleship.player1hits)
            battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)

            # AI move logic
            print("AI is making a move...")
            ai_move = ai.make_move(battleship.player2TargetBoard, battleship.player1ShipBoard, battleship.player2hits, battleship.player2misses)
            battleship.checkForCollision(battleship.player2TargetBoard, battleship.player1ShipBoard, ai_move, battleship.player2hits, battleship.player2misses, battleship.player1placedShips, battleship.copyPlayer1placedShips)
            battleship.player1Turn = True  # Switch back to Player 1 after AI's move
            pygame.time.wait(1000)  # Delay for tension

        # Handle user events and clicks
        keys = pygame.key.get_pressed()
        event = pygame.event.poll()

        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            pygame.mixer.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Player 1's turn, handle input
            if battleship.player1Turn:
                battleship.ACHANNEL.play(battleship.CAUDIO)
                pygame.time.delay(1000)
                played = battleship.checkForCollision(battleship.player1TargetBoard, battleship.player2ShipBoard, pos, battleship.player1hits, battleship.player1misses, battleship.player2placedShips, battleship.copyPlayer2placedShips)
                if played:
                    # Update the boards
                    battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
                    battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
                    add_text.add_labels_middle(battleship.SCREEN)
                    add_text.add_labels_ships(battleship.SCREEN)
                    pygame.display.update()

                    sunkenShip = battleship.shipSunk(battleship.copyPlayer2placedShips)
                    if sunkenShip:
                        add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                        pygame.display.update()
                        if battleship.gameIsOver(battleship.copyPlayer2placedShips):
                            battleship.gameover = True
                            add_text.add_text(battleship.SCREEN, 'Player 1 won!')
                            pygame.display.update()
                            pygame.time.wait(2000)
                            add_text.ask_play_again(battleship.SCREEN)

                    pause(1)
                    if not battleship.gameover:
                        add_text.add_black_screen(battleship.SCREEN)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        pygame.event.clear()  # Clear the queue after the black screen
                    battleship.player1Turn = False

        pygame.display.update()

    print("Out of loop")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    battleship.gameover = False
                    battleship.player1Turn = True
                    battleship.player1ready = False
                    battleship.player2ready = False
                    battleship.player1hits = []
                    battleship.player1misses = []
                    battleship.player2hits = []
                    battleship.player2misses = []
                    battleship.player1placedShips = []
                    battleship.player2placedShips = []
                    battleship.player1ships = []
                    battleship.player2ships = []
                    battleship.SCREEN.fill((0,0,0))
                    pygame.display.update()
                    run()
                    break
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()
                    break
