from matplotlib.pyplot import pause
import pygame
import sys
# rgb colors
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)

# font text is from https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# learned how to do text in pygame and based code off of https://stackoverflow.com/questions/10467863/how-to-remove-replace-text-in-pygame
# adds text to top of screen
def add_text(screen, text):
    # fills the screen black in the area wanted so that previous text doesn't show up still
    screen.fill(BLACK, (0, 0, 430, 80))
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render(text, True, RED)
    textRect = text.get_rect()
    textRect.center = (245, 15)
    screen.blit(text, textRect)
# adds screen to not show other player's ships in between turns
def add_black_screen(screen):
    screen.fill(BLACK, (0,0, 490, 400))
    add_text(screen, 'Switching turns, do not cheat!')
# called if the player has taken too long to place ships
# displays that game will be ending
def time_out(screen):
    screen.fill(BLACK, (0,0, 430, 490))
    font = pygame.font.Font('freesansbold.ttf', 14)
    text = font.render("You took too long to choose the next valid spot for your ship!", True, RED)
    textRect = text.get_rect()
    textRect.center = (245, 200)
    screen.blit(text, textRect)
    text = font.render("The game will automatically exit in 3 seconds!", True, RED)
    textRect = text.get_rect()
    textRect.center = (245, 220)
    screen.blit(text, textRect)

# adds column labels to ship screen
def add_labels_ships(screen):
    screen.fill(BLACK, (30,90, 190, 8))
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for x in range(40, 230, 20):
        text = font.render(letters[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (x, 90)
        screen.blit(text, textRect)
        counter = counter + 1

# adds column labels to target screen
def add_labels_targets(screen):
    screen.fill(BLACK, (270,90, 190, 8))
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for x in range(270, 460, 20):
        text = font.render(letters[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (x, 90)
        screen.blit(text, textRect)
        counter = counter + 1

# adds row labels to middle of screen
def add_labels_middle(screen):
    screen.fill(BLACK, (240,110, 8, 200))
    nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    counter = 0
    font = pygame.font.Font('freesansbold.ttf', 16)
    for y in range(110, 300, 20):
        text = font.render(nums[counter], True, RED)
        textRect = text.get_rect()
        textRect.center = (245, y)
        screen.blit(text, textRect)
        counter = counter + 1
