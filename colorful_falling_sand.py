import pygame as pg
import sys
from random import randint

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Button:
    def __init__(self, x, y, width, height, text, action):
        """
        Initializes the button with the given parameters.

        Parameters:
            x (int): The x-coordinate of the button.
            y (int): The y-coordinate of the button.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text to be displayed on the button.
            action (function): The action to be performed when the button is clicked.
        """
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pg.font.Font(None, 36)
        self.color = WHITE
        self.highlighted_color = RED

    def draw(self, screen):
        """
        Draw a rectangle with the specified color and border on the screen, and blit the text onto it.
        
        Args:
            screen: The screen surface to draw on.
        
        Returns:
            None
        """
        pg.draw.rect(screen, self.color, self.rect)
        pg.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

# Initialize Pygame
pg.init()

# Set up display
width, height = 600, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Colorful Falling Sand")

# Set grid parameters
grid_size = 5
grid_rows = height // grid_size
grid_columns = width // grid_size
colored_cell = [
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (75, 0, 130),  # Indigo
    (148, 0, 211),  # Violet
]
colored_cell_index = 0
empty_cell = (0, 0, 0)
background_color = (0, 0, 0)
changing_color_counter = 200
counter = 0

# Initialize a 2D grid with zero values (representing colors)
grid = [[(0, 0, 0) for _ in range(grid_columns)] for _ in range(grid_rows)]


# Function to change the color of a specific cell in the grid
def change_color(row, col, color):
    """
    A function to change the color of a specific cell in the grid.
    
    Parameters:
    - row: the row index of the cell
    - col: the column index of the cell
    - color: the new color to assign to the cell
    
    Return:
        None
    """
    grid[row][col] = color


# Function to get the row and column from mouse coordinates
def get_grid_position(mouse_x, mouse_y):
    """
    Calculate the grid position based on the mouse coordinates.

    Parameters:
    mouse_x (int): The x-coordinate of the mouse.
    mouse_y (int): The y-coordinate of the mouse.

    Returns:
    tuple: A tuple containing the row and column of the grid position.
    """
    row = mouse_y // grid_size
    col = mouse_x // grid_size
    return row, col

# check if there is a difference between current grid(phase) and previous grid(phase)
def check_empty_position(row, col):
    """
    Check if the position at the given row and column is an empty cell and the cell above it is not empty.
    Parameters:
    - row: an integer representing the row index
    - col: an integer representing the column index
    Returns:
    - a boolean indicating whether the condition is met
    """
    return grid[row][col] == empty_cell and grid[row-1][col] != empty_cell

def check_empty_sides(row, col):
    """
    Check if the current cell and its adjacent cells are empty or not.
    
    Args:
    row (int): The row index of the current cell.
    col (int): The column index of the current cell.
    
    Returns:
    bool: True if the current cell and its adjacent cells are not empty, False otherwise.
    """
    # Check if the current cell is not empty
    current_cell_not_empty = grid[row][col] != empty_cell 
    # Check if the upper cell is not empty
    upper_cell_not_empty = grid[row - 1][col] != empty_cell
    # Check if the left cell is empty
    left_cell_empty = col - 1 >= 0 and grid[row][col - 1] == empty_cell
    # Check if the right cell is empty
    right_cell_empty = col + 1 < grid_columns and grid[row][col + 1] == empty_cell
    # Return True if the current cell and upper cell are not empty, and at least one of the adjacent cells is empty
    return current_cell_not_empty and upper_cell_not_empty and (left_cell_empty or right_cell_empty)


def clear_screen():
    """
    Clears the screen and resets the grid to a 2D list of tuples representing RGB color values.
    """
    global grid
    screen.fill(background_color)
    grid = [[(0, 0, 0) for _ in range(grid_columns)] for _ in range(grid_rows)]

# Create a button
button = Button(580, 30, 100, 40, "Clear", clear_screen)

def draw_grid():
    """
    Draws a grid on the screen using the given grid data, and also draws a button on the screen.
    """
    global button
    for row in range(grid_rows):
        for col in range(grid_columns // 2):
            # Draw from the front
            rect_front = pg.Rect(col * grid_size, row * grid_size, grid_size, grid_size)
            pg.draw.rect(screen, grid[row][col], rect_front)

            # Draw from the back
            col_back = grid_columns - 1 - col
            rect_back = pg.Rect(col_back * grid_size, row * grid_size, grid_size, grid_size)
            pg.draw.rect(screen, grid[row][col_back], rect_back)
            
    button = Button(260, 30, 100, 40, "Clear", clear_screen)
    # Draw the button
    button.draw(screen)

def change_position_of_colored_cell():
    """
    Change the position of colored cells in the grid based on certain conditions.
    """
    for c in range(grid_columns):
        for r in range(grid_rows - 1, 0, -1):
            if check_empty_position(r, c):
                change_color(r, c, grid[r - 1][c])
                change_color(r - 1, c, empty_cell)
            elif check_empty_sides(r, c):
                a = c - 1 >= 0 and grid[r][c - 1] == empty_cell
                b = c + 1 < grid_columns and grid[r][c + 1] == empty_cell
                if a and b:
                    x = randint(0, 1)
                    if x == 0:
                        change_color(r, c - 1, grid[r - 1][c])
                        change_color(r - 1, c, empty_cell)
                    else:
                        change_color(r, c + 1, grid[r - 1][c])
                        change_color(r - 1, c, empty_cell)
                elif a:
                    change_color(r, c - 1, grid[r - 1][c])
                    change_color(r - 1, c, empty_cell)
                elif b:
                    change_color(r, c + 1, grid[r - 1][c])
                    change_color(r - 1, c, empty_cell)

# Main game loop
if __name__ == '__main__':
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            button.handle_event(event)

        # Draw the button
        button.draw(screen)

        if event.type == pg.MOUSEMOTION:
            mouse_x, mouse_y = pg.mouse.get_pos()
            row, col = get_grid_position(mouse_x, mouse_y)
            if grid[row][col] == empty_cell:
                counter += 1
                if counter >= changing_color_counter:
                    colored_cell_index = (colored_cell_index + 1) % 7
                    counter = 0  
                # Change color to the next color when clicked
                change_color(row, col, colored_cell[colored_cell_index])  

        # Draw the grid
        draw_grid()

        # change position of colored cell if the cell below it is empty
        change_position_of_colored_cell()

        # Update the display
        pg.display.flip()
