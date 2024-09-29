import copy
from operator import truediv
from matplotlib.pyplot import pause
import pygame
import sys
import add_text
import place_ships
import get_ships_num
import battleship
import easy
import medium

def run():
    print("singleplayer")
    arrays = get_ships_num.get_ships(battleship.player1ships, battleship.player2ships, battleship.SCREEN, battleship.player1placedShips, battleship.player2placedShips)
    battleship.player1ships = arrays[0]
    battleship.player2ships = arrays[1]
    battleship.player1placedShips = arrays[2]
    battleship.player2placedShips = arrays[3]
    clock = pygame.time.Clock()
    easy_ai = easy.EasyAI()
    ai = medium.MediumAI()
    ship_hit = False

    while not battleship.gameover:
        pos = pygame.mouse.get_pos()
        
        if not battleship.player1ready:
            place_ships.placePlayer1Ships(battleship.SCREEN, battleship.player1ships, battleship.player1placedShips, battleship.player1ShipBoard)
            battleship.player1ready = True
            battleship.copyPlayer1placedShips = copy.deepcopy(battleship.player1placedShips)
        
        if not battleship.player2ready:
            place_ships.placePlayer2Ships(battleship.SCREEN, battleship.player2ships, battleship.player2placedShips, battleship.player2ShipBoard)
            battleship.player2ready = True
            battleship.copyPlayer2placedShips = copy.deepcopy(battleship.player2placedShips)

        add_text.add_text(battleship.SCREEN, 'Battleship')
        
        if battleship.player1Turn:
            add_text.add_text(battleship.SCREEN, 'Player 1 Turn')
            battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
            battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
            add_text.add_labels_middle(battleship.SCREEN)
            add_text.add_labels_ships(battleship.SCREEN)

        keys = pygame.key.get_pressed()
        event = pygame.event.poll()
        
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            pygame.mixer.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if battleship.player1Turn:
                battleship.ACHANNEL.play(battleship.CAUDIO)
                pygame.time.delay(1000)
                played = battleship.checkForCollision(battleship.player1TargetBoard, battleship.player2ShipBoard, pos, battleship.player1hits, battleship.player1misses, battleship.player2placedShips, battleship.copyPlayer2placedShips)
                if played:
                    battleship.printShipBoard(battleship.player1ShipBoard, battleship.player1placedShips, battleship.player2hits)
                    battleship.printBoard(battleship.player1TargetBoard, battleship.player1hits, battleship.player1misses)
                    pygame.display.update()
                    sunkenShip = battleship.shipSunk(battleship.copyPlayer2placedShips)
                    if sunkenShip:
                        add_text.add_text(battleship.SCREEN, 'You sunk a ship!')
                        pygame.display.update()
                        ended = battleship.gameIsOver(battleship.copyPlayer2placedShips)
                        if ended:
                            battleship.gameover = True
                            add_text.add_text(battleship.SCREEN, 'Player 1 won!')
                            pygame.display.update()
                            pygame.time.wait(2000)
                            add_text.ask_play_again(battleship.SCREEN)
                    pause(1)
                    if not battleship.gameover:
                        add_text.add_black_screen(battleship.SCREEN)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        pygame.event.clear()
                    battleship.player1Turn = False
                if not battleship.gameover:
                    add_text.add_text(battleship.SCREEN, 'AI is making a move...')
                    pygame.display.update()
                    pygame.time.delay(1000)
                    previous_hits_length = len(battleship.player2hits)
                    row, col = ai.make_move(ship_hit)
                    played = ai.checkForCollision(battleship.player2TargetBoard, battleship.player1ShipBoard, row, col, battleship.player2hits, battleship.player2misses, battleship.player1placedShips, battleship.copyPlayer1placedShips)
                    if len(battleship.player2hits) > previous_hits_length:
                        print("Ship hit on last turn.")
                        ship_hit = True
                        ai.update_last_hit(row, col)
                    if played:
                        battleship.printBoard(battleship.player2TargetBoard, battleship.player2hits, battleship.player2misses)
                        pygame.display.update()
                        sunkenShip = battleship.shipSunk(battleship.copyPlayer1placedShips)
                        if sunkenShip:
                            add_text.add_text(battleship.SCREEN, 'AI sunk a ship!')
                            ship_hit = False
                            pygame.display.update()
                            ended = battleship.gameIsOver(battleship.copyPlayer1placedShips)
                            if ended:
                                battleship.gameover = True
                                add_text.add_text(battleship.SCREEN, 'Player 2 won!')
                                pygame.display.update()
                                pygame.time.wait(2000)
                                add_text.ask_play_again(battleship.SCREEN)
                        pause(1)
                        if not battleship.gameover:
                            add_text.add_black_screen(battleship.SCREEN)
                            pygame.display.update()
                            pygame.time.wait(2000)
                            pygame.event.clear()
                        battleship.player1Turn = True

        pygame.display.update()

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
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

