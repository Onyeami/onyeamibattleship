# Import the random module to generate random
import random


# Function to create a grid of given size filled with 'o'
def create_grid(size):
    return [['o'] * size for _ in range(size)]


# Function to print the grid in a nice format
def print_grid(grid):
    size = len(grid)
    # Print column headers (A, B, C, ...)
    print("  " + " ".join([chr(65+i) for i in range(size)]))
    print("  " + "-" * (2*size+1))  # print line separator


# Function to place a given number of ships ('s') randomly in the grid
def place_ships(grid, num_ships):
    size = len(grid)
    for _ in range(num_ships):
        ship_row = random.randint(0, size-1)
        ship_col = random.randint(0, size-1)
        # Ensure not to place a ship on top of another
        while grid[ship_row][ship_col] == 's':
            ship_row = random.randint(0, size-1)
            ship_col = random.randint(0, size-1)
        grid[ship_row][ship_col] = 's'  # Place the ship


# Function to check if a guess is within the grid boundaries
def is_valid_guess(guess, size):
    row, col = guess
    return row >= 0 and row < size and col >= 0 and col < size 