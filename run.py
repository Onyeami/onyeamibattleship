# Import the random module to generate random numbers
import random
import time


# Function to create a grid of given size filled with 'o'
def create_grid(size):
    return [['o'] * size for _ in range(size)]


# Function to print the grid in a nice format
def print_grid(grid):
    size = len(grid)
    # Print column headers (A, B, C, ...)
    print("   " + " ".join([chr(65+i) for i in range(size)]))

    for i in range(size):
        # Print each row with row number
        print(str(i+1).rjust(2) + "|" + " ".join(grid[i]) + "|")
        print("-" * (2*size+5))  # Print line separator


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


# Function for the computer's turn to guess
def computer_guess(size, guessed_cells):
    while True:
        guess_row = random.randint(0, size-1)
        guess_col = random.randint(0, size-1)
        guess = (guess_row, guess_col)
        if guess not in guessed_cells:
            return guess


# Function to play the game
def play_game(size, num_ships, level):
    player_score = 0  # Initialize player's score
    computer_score = 0  # Initialize computer's score
    player_grid = create_grid(size)  # Create the player's game grid
    computer_grid = create_grid(size)  # Create the computer's game grid
    place_ships(player_grid, num_ships)  # Place the player's ships
    place_ships(computer_grid, num_ships)  # Place the computer's ships
    print("Welcome to Battleships!")  # Welcome message
    print("Try to sink all the ships.")  # Game instructions
    print("Your grid:")
    print_grid(player_grid)  # Print the initial game state
    turns = 0  # Initialize turn counter
    player_guessed_cells = set()  # Keep track of player's guessed cells
    computer_guessed_cells = set()  # Keep track of computer's guessed cells
    while True:  # Game loop
        start_time = time.time()
        guess_row_input = input("Guess row (1-{}): ".format(size))
        if time.time() - start_time > level:
            print("You didn't respond in time! You lose your turn.")
            continue
        guess_row = int(guess_row_input) - 1
        start_time = time.time()
        guess_col_input = input("Guess column (A-{}): ".format(chr(64+size)))
        if time.time() - start_time > level:
            print("You didn't respond in time! You lose your turn.")
            continue
        guess_col = ord(guess_col_input.upper()) - 65
        player_guess = (guess_row, guess_col)
        if not is_valid_guess(player_guess, size):
            print("Invalid guess! Try again.")
            continue
        if player_guess in player_guessed_cells:
            print("You have already guessed this cell. Try again.")
            continue
        player_guessed_cells.add(player_guess)
        turns += 1
        if is_hit(player_guess, computer_grid):
            print("Congratulations! You hit a ship!")
            computer_grid[guess_row][guess_col] = 'x'
            print("Computer's grid:")
            print_grid(computer_grid)
            player_score += 1  # Increment player's score
            if all(all(cell != 's' for cell in row) for row in computer_grid):
                print("You sunk all the ships in {} turns!".format(turns))
                break
        else:
            print("Sorry, you missed.")
            player_grid[guess_row][guess_col] = 'm'
            print("Your grid:")
            print_grid(player_grid)

        # Computer's turn to guess
        comp_guess = computer_guess(size, computer_guessed_cells)
        computer_guessed_cells.add(comp_guess)

        if is_hit(comp_guess, player_grid):
            print("Computer hit your ship!")
            player_grid[comp_guess[0]][comp_guess[1]] = 'x'
            print("Your grid:")
            print_grid(player_grid)
            computer_score += 1  # Increment computer's scores

            if all(all(cell != 's' for cell in row) for row in player_grid):
                print("Computer sunk all your ships in {} turns!".format(turns))
                break
            else:
                print("Computer missed.")
                player_grid[comp_guess[0]][comp_guess[1]] = 'm'
                print("Your grid:")
                print_grid(player_grid)
            print("Final Scores - Player: {}, Computer: {}".format(player_score, computer_score))


# Main function to start the game
def main():
    size = int(input("Enter the grid size: "))
    max_ships = size*size - 2
    print("You can place up to {} ships.".format(max_ships))
    num_ships = int(input("Enter the number of ships (1-{}): ".format(max_ships)))
    while num_ships > max_ships:
        print("Too many ships! Try again.")
        num_ships = int(input("Enter the number of ships (1-{}): ".format(max_ships)))
    level = 30  # Default level: Low level

    game_counter = 0  # Keep track of the number of games played

    for i in range(1, 31):
        if game_counter >= 20:
            level = 10  # Critical level
        elif game_counter >= 10:
            level = 20  # Medium level

        print("Starting game {}. Level: {}".format(i, level))
        play_game(size, num_ships, level)

        game_counter += 1


if __name__ == "__main__":
    main()