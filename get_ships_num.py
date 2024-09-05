from audioop import add
import math
from matplotlib.pyplot import pause
from numpy import place
import pygame
import sys
import battleship
import add_text
# rgb colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

# handles getting how many ships the user wants
def get_ships(player1ships, player2ships, screen, player1ships2d, player2ships2d):

    # adds text 
    add_text.add_text(screen, 'Choose How Many Ships You Would Like')
    # start at false
    optionsChosen = False
    # place the boxes for options
    place_options(screen)
    # while nothing has been chosen
    while not optionsChosen:
        # get the position
         pos = pygame.mouse.get_pos()
         for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # get the box that was selected and assign ships accordingly
                    index = get_index(screen, pos) 
                    if index != -1:
                        optionsChosen = True # set optionsChosen to true so loop will end
                        screen.fill(BLACK, (0, 0, 490, 400))
                        print(index)
                        if index == 1:
                            # 1x1
                            player1ships=[1]
                            player2ships=[1]   
                            player1ships2d = [[]]
                            player2ships2d = [[]]
                        elif index == 2:
                            # 1X1, 2X1
                            player1ships=[1,2]
                            player2ships=[1,2] 
                            player1ships2d = [[],[]]
                            player2ships2d = [[],[]] 
                        elif index == 3:
                            player1ships=[1,2,3]
                            player2ships=[1,2,3] 
                            player1ships2d = [[],[],[]]
                            player2ships2d = [[],[],[]]
                        elif index == 4:
                            player1ships=[1,2,3,4]
                            player2ships=[1,2,3,4] 
                            player1ships2d = [[],[],[], []]
                            player2ships2d = [[],[],[], []]
                        elif index == 5:
                            player1ships=[1,2,3,4,5]
                            player2ships=[1,2,3,4,5] 
                            player1ships2d = [[],[],[], [],[]]
                            player2ships2d = [[],[],[], [],[]]           
         pygame.display.update()
    # returns all the necessary arrays
    return (player1ships, player2ships, player1ships2d, player2ships2d)

# creates rectangles for user to click and choose num of ships
def place_options(screen):
    # used offset to move squares to center
    offset = 45
    # create rects for each choice
    rect1 = pygame.Rect(10+offset,200,50,50)
    rect2 = pygame.Rect(90+offset,200,50,50)
    rect3 = pygame.Rect(170+offset,200,50,50)
    rect4 = pygame.Rect(250+offset,200,50,50)
    rect5 = pygame.Rect(330+offset,200,50,50)
    # draw each rect
    pygame.draw.rect(screen, WHITE, rect1, 1)
    pygame.draw.rect(screen, WHITE, rect2, 1)
    pygame.draw.rect(screen, WHITE, rect3, 1)
    pygame.draw.rect(screen, WHITE, rect4, 1)
    pygame.draw.rect(screen, WHITE, rect5, 1)
    # add text to boxes
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('1', True, RED)
    textRect = text.get_rect()
    textRect.center = (35+offset, 225)
    screen.blit(text, textRect)
    text = font.render('2', True, RED)
    textRect = text.get_rect()
    textRect.center = (115+offset, 225)
    screen.blit(text, textRect)
    text = font.render('3', True, RED)
    textRect = text.get_rect()
    textRect.center = (195+offset, 225)
    screen.blit(text, textRect)
    text = font.render('4', True, RED)
    textRect = text.get_rect()
    textRect.center = (275+offset, 225)
    screen.blit(text, textRect)
    text = font.render('5', True, RED)
    textRect = text.get_rect()
    textRect.center = (355+offset, 225)
    screen.blit(text, textRect)

# gets the index of the user click so that we know what box they selected
def get_index(screen, pos):
    offset = 45
    rect1 = pygame.Rect(10+offset,200,50,50)
    rect2 = pygame.Rect(90+offset,200,50,50)
    rect3 = pygame.Rect(170+offset,200,50,50)
    rect4 = pygame.Rect(250+offset,200,50,50)
    rect5 = pygame.Rect(330+offset,200,50,50)
    # collide point checks if pos is within the rect object
    # based off of https://stackoverflow.com/questions/7415109/creating-a-rect-grid-in-pygame
    if rect1.collidepoint(pos):
        return 1
    elif rect2.collidepoint(pos):
        return 2
    elif rect3.collidepoint(pos):
        return 3
    elif rect4.collidepoint(pos):
        return 4
    elif rect5.collidepoint(pos):
        return 5
    else:
        return -1

