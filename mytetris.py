import pygame
import random

pygame.font.init()

"""
Description     This Tetris Game is going to be of a 10 x 20 grid with 7 different shapes (S, Z, I, O, L, J, T) falling from the top.
Features        The game will have a title, 'Tetris', score counter, 'score: ', and the next shape indicator, 'next shape: '.
"""

""" Setting the screen & gameplay grid dimensions as GLOBAL VARIABLES """
screen_width = 800
screen_height = 700
play_width = 300        # 300 // 10 = 30 width per block
play_height = 600       # 600 // 20 = 30 height per block
block_size = 30

top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height 

""" Shape structures & their different rotational layout in the form of a list with a 5 x 5 grid format """
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

""" Putting these shapes together in a list """
shapes = [S, Z, I, O, L, J, T]

""" Colour of shapes later put together in a list """
salmon = (250,128,114)
honey_dew = (240,255,240)
alice_blue = (240,248,255)
moccasin = (255,228,181)
tomato = (255,99,71)
royal_blue =(65,105,225)
pale_violet_red = (219,112,147)

shape_colors = [honey_dew, salmon, alice_blue, moccasin, tomato, royal_blue, pale_violet_red]
# Giving each shape a specific color depending on its index in the list




""" Introducing class to represent different pieces """
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.colour = shape_colors[shapes.index(shape)]
        self.rotation = 0
        # default rotation is going to be 0 so that everytime we add 1, it's going to represent the next rotational layout of the shape we want from the list



""" Introducing a function to create the grid we want; this is done by creating a list full of colours """
def create_grid(locked_pos = {}):
    """ Creating a 2D list where the second dimension is going to represent a bunch of colours """
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]          # creating one list for every row in our grid, so since we have 20 rows, we want to create 20 sublists and each of these sublists are going to have 10 coloured squares.
    
    """ Checking blocks that are in locked position, i.e. are static or already fallen and changing the grid colour to the corresponding block """
    for i in range(len(grid)):                                          # i - row number/y-value
        for j in range(len(grid[i])):                                   # j - column number/x-value
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c

    return grid



""" Creating a function that converts the shape of blocks from list format to game block format """
# Get clear understanding of this function later
def convert_shape_format(shape):
    positions = []                                                      # creating an empty list to generate a list of positions
    format = shape.shape[shape.rotation % len(shape.shape)]             # creating a list to get the sublists of the desired shape

    """ Creating a for loop to go through every column and every row and do something based on if there is a 0 or a period """
    for i, line in enumerate(format):
        row = list(line)                                                # converting each line into a list format
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))            # adding the current value (whatever column/row we are in) of our shape to the 'j' and 'i' value in the positions list

    """ Giving the positions an offset """
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions



""" Creating a function to check for empty valid spaces in the grid """
def valid_space(shape, grid):
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_pos = [j for sub in valid_pos for j in sub]                   # converting the 2D valid_pos list into a 1D list, i.e. flattening the list
    
    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape:
        if pos not in valid_pos:
            if pos[1] > -1:                                             # position will only be valid if Y-value > -1
                return False
    
    return True



""" Creating a function to check if any of the Y-values are above 0, i.e. if the blocks have hit the top of the grid """
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False



""" Creating a function to get shapes randomly """
def get_shape():
    return Piece(5, 0, random.choice(shapes))



""" Creating a function to draw text in the main menu """
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("Gotham", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (screen_width/2 - (label.get_width()/2), screen_height/2 - (label.get_height()/2)))



""" Creating a function to draw all the lines for the grid """
def draw_gridlines(surface, grid):

    for i in range(len(grid)):
        pygame.draw.line(surface, (255, 250, 250), (top_left_x, top_left_y + i*block_size), (top_left_x + play_width, top_left_y + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (255, 250, 250), (top_left_x + j*block_size, top_left_y), (top_left_x + j*block_size, top_left_y + play_height))



""" Creating a function to clear the row that has been filled in the grid """
def clear_rows(grid, locked):
    increment = 0
    
    for i in range(len(grid) - 1, -1, -1):                              # looping through the grid backwards
        row = grid[i]
        if (0, 0, 0) not in row:
            increment += 1
            ind = i
            """ Deleting the filled row """
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    """ Shifting every row """
    if increment > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment



""" Creating a function that shows the next incoming shape """
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("Gotham", 30)
    label = font.render("Next Shape:", 1, (255, 255, 255))
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.colour, (top_left_x + play_width + 50 + j*block_size, top_left_y + play_height/2 - 100 + i*block_size, block_size, block_size), 0)

    surface.blit(label, (top_left_x + play_width + 50 + 10, top_left_y + play_height/2 - 100 - 30))



""" Keeping tabs of score from a score text file """
def update_score(new_score):
    with open('score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open('score.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


""" """
def max_score():
    with open('score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score



""" Creating a function that draws the window when the game starts """
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))                                             # Fills the whole surface that we are working in with black colour

    """ Drawing the title 'Tetris' on the screen """
    font = pygame.font.SysFont('Gotham', 70)                            # creating a font with the type and size
    label = font.render("TETRIS", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 30))

    score_font = pygame.font.SysFont("Gotham", 30)
    score_label = score_font.render("Score: " + str(score), 1, (255, 255, 255))

    surface.blit(score_label, (top_left_x + play_width + 50 + 10, top_left_y + play_height/2 + 150 - 50))

    high_score_font = pygame.font.SysFont("Gotham", 30)
    high_score_label = high_score_font.render("High Score: " + str(last_score), 1, (255, 255, 255))

    surface.blit(high_score_label, (top_left_x + play_width + 50 + 10, top_left_y + play_height/2 + 200 - 50))

    for i in range(len(grid)):                                          
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    draw_gridlines(surface, grid)

    """ Drawing a coloured border around the gameplay grid """
    pygame.draw.rect(surface, (205,92,92), (top_left_x, top_left_y, play_width, play_height), 4)



""" """
def main(win):

    last_score = max_score()

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27                                                   # how long it takes before each shape starts falling
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)                            # reason we're doing this again is because everytime we move, we have a chance of adding something to the locked position
        fall_time += clock.get_rawtime()                                # clock.raw_time() gets the amount of time since the last clock.tick() runs in every while loop
        level_time += clock.get_rawtime()
        clock.tick()

        """ Increasing the fall_speed of blocks every 5 sec """
        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01


        """ Allowing the piece to automatically move down the grid """
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                        
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1

                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        """ Checking all the positions of the piece moving down to see if we've hit the ground or if we need to lock it; and adding color to the grid so we can see the piece """
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:          
                grid[y][x] = current_piece.colour

        """ Updating locked_positions """
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.colour                  # this is going to give us a dict like {(1, 2):(255, 0, 0)}
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False                                            # change_piece = False because we're onto a new piece that will spawn at the top of the screen

            score += clear_rows(grid, locked_positions) * 10
        
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False 

            update_score(score)



""" """
def main_menu(win):
    run = True

    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, "Press Any Key To Play", 60, (255, 255, 255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

""" Initializing a window/screen for display """
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
main_menu(win)