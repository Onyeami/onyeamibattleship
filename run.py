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


# Function to check if a guess hits a ship
def is_hit(guess, grid):
    row, col = guess
    return grid[row][col] == 's'


# Function to play the game
def play_game(size, num_ships):
    grid = create_grid(size)  # Create the game grid
    place_ships(grid, num_ships)  # Place the ships
    print("Welcome to Battleships!")  # Welcome message
    print("Try to sink all the ships.")  # Game instructions
    print_grid(grid)  # Print the initial game state
    turns = 0  # Initialize turn counter
    guessed_cells = set()  # Keep track of guessed cells
    while True:  # Game loop
        # Get user's guess for row
        guess_row = int(input("Guess row (1-{}): ".format(size))) - 1
        # Get user's guess for column
        guess_col = ord(input("Guess column (A-{}): ".format(chr(64+size)))) - 65
        guess = (guess_row, guess_col)  # Form the guess pair (row, column)
        if not is_valid_guess(guess, size):  # Check if the guess is valid
            print("Invalid guess! Try again.")
            continue
        if guess in guessed_cells:  # Check if the cell was already guessed
            print("You have already guessed this cell. Try again.")
            continue
        # Add the guessed cell to the set of guessed cells
        guessed_cells.add(guess)
        turns += 1  # Increment turn counter
        if is_hit(guess, grid):  # Check if the guess hits a ship
            print("Congratulations! You hit a ship!")
            grid[guess_row][guess_col] = 'x'  # Mark hit cells with 'x'
            print_grid(grid)
            # Check if all ships are sunk
            if all(all(cell != 's' for cell in row) for row in grid):
                print("You sunk all the ships in {} turns!".format(turns))
                break
        else:
            print("Sorry, you missed.")
            grid[guess_row][guess_col] = 'm'  # Mark missed cells with 'm'
            print_grid(grid)


# Main function to start the game            
def main():
    size = int(input("Enter the grid size: "))
    max_ships = size*size - 2
    print("You can place up to {} ships.".format(max_ships))
    num_ships = int(input("Enter the number of ships (1-{}): ".format(max_ships)))
    while num_ships > max_ships:
        print("Too many ships! Try again.")
        num_ships = int(input("Enter the number of ships (1-{}): ".format(max_ships)))
    play_game(size, num_ships)


# This line means that main() will be called when this script is run directly.
if __name__ == "__main__":
    main()
