import random
import time



def create_grid(size):
    return [['o'] * size for _ in range(size)]

def print_grid(grid):
    size = len(grid)
    print("   " + " ".join([chr(65+i) for i in range(size)]))

    for i in range(size):
        print(str(i+1).rjust(2) + "|" + " ".join(grid[i]) + "|")

    print("-" * (2*size+5))
    
def place_ships(grid, num_ships):
    size = len(grid)
    max_ships = size * size - 2  # Maximum number of ships allowed

    if num_ships > max_ships:
        print("Invalid number of ships! Maximum allowed ships:", max_ships)
        return

    for _ in range(num_ships):
        ship_row = random.randint(0, size - 1)
        ship_col = random.randint(0, size - 1)
        while grid[ship_row][ship_col] == 's':
            ship_row = random.randint(0, size - 1)
            ship_col = random.randint(0, size - 1)
        grid[ship_row][ship_col] = 's'
        
def is_valid_guess(guess, size):
    row, col = guess
    return row >= 0 and row < size and col >= 0 and col < size

def is_hit(guess, grid):
    row, col = guess
    return grid[row][col] == 's'

def computer_guess(size, guessed_cells):
    while True:
        guess_row = random.randint(0, size-1)
        guess_col = random.randint(0, size-1)
        guess = (guess_row, guess_col)
        if guess not in guessed_cells:
            return guess

def check_ship_hit(guess, grid):
    row, col = guess
    return grid[row][col] == 's'




def play_game(size, num_ships, level, time_limit):
    size = get_user_input("Enter the grid size (e.g., 5 for a 5x5 grid): ", type_=int, min_=1)
    num_ships = get_user_input("Enter the number of ships: ", type_=int, min_=1, max_=size * size)
    player_score = 0
    computer_score = 0
    player_grid = create_grid(size)
    computer_grid = create_grid(size)
    place_ships(player_grid, num_ships)
    place_ships(computer_grid, num_ships)
    print("Welcome to Battleships!")
    print("Try to sink all the ships.")
    print("Your grid:")
    print_grid(player_grid)
    turns = 0
    player_guessed_cells = set()
    computer_guessed_cells = set()
    player_hits = 0
    player_misses = 0
    computer_hits = 0
    computer_misses = 0
    player_ships = num_ships
    computer_ships = num_ships
    game_history = []
    in_game_menu = False  # Flag to indicate whether in-game menu is active

    while True:
        
        if not in_game_menu:
            # Player's turn
            print("Player's turn:")
            start_time = time.time()
            guess = input("Enter your guess (e.g., A1) or type 'status' to check the current status: ").upper()

            if guess == 'STATUS':
                display_game_status(player_hits, player_misses, player_ships, computer_hits, computer_misses, computer_ships)
                continue

            guess_col = ord(guess[0]) - ord('A')
            guess_row = int(guess[1:]) - 1
            guess_coords = (guess_row, guess_col)

            if not is_valid_guess(guess_coords, size):
                print("Invalid guess. Try again.")
                continue

            elapsed_time = time.time() - start_time

            if elapsed_time > time_limit:
                print("Time's up! It's the computer's turn now.")
            else:
                if guess_coords in player_guessed_cells:
                    print("You already guessed that cell. Try again.")
                    continue

                player_guessed_cells.add(guess_coords)
                game_history.append(("Player", guess_coords))

                if is_hit(guess_coords, computer_grid):
                    print("You hit a ship!")
                    player_score += 1
                    player_hits += 1
                    computer_ships -= 1
                    computer_grid[guess_row][guess_col] = 'x'
                else:
                    print("You missed!")
                    player_misses += 1
                    player_grid[guess_row][guess_col] = 'x'

                turns += 1
                print("Computer's grid:")
                print_grid(computer_grid)

                if player_ships == 0 or computer_ships == 0:
                    break

        # Computer's turn
        print("Computer's turn:")
        start_time = time.time()

        # Add a delay for suspense, you can remove this if not needed
        time.sleep(1)

        guess_coords = computer_guess(size, computer_guessed_cells)

        elapsed_time = time.time() - start_time

        if elapsed_time > time_limit:
            print("Time's up! Your turn again.")
            continue

        if guess_coords in computer_guessed_cells:
            continue

        computer_guessed_cells.add(guess_coords)
        game_history.append(("Computer", guess_coords))

        if is_hit(guess_coords, player_grid):
            print("Computer hit one of your ships!")
            computer_score += 1
            computer_hits += 1
            player_ships -= 1
            player_grid[guess_coords[0]][guess_coords[1]] = 'x'
        else:
            print("Computer missed!")
            computer_misses += 1
            player_grid[guess_coords[0]][guess_coords[1]] = 'o'

        turns += 1
        print("Your grid:")
        print_grid(player_grid)

        if player_ships == 0 or computer_ships == 0:
            break

    # Determine the winner as before
    if player_score > computer_score:
        winner = "Player"
    elif computer_score > player_score:
        winner = "Computer"
    else:
        winner = "Nobody"  # It's a tie

    print("Game over!")
    print("Player score:", player_score)
    print("Computer score:", computer_score)
    print("Player hits:", player_hits)
    print("Player misses:", player_misses)
    print("Player remaining ships:", player_ships)
    print("Computer hits:", computer_hits)
    print("Computer misses:", computer_misses)
    print("Computer remaining ships:", computer_ships)
    print("Winner:", winner)

    print("Game history:")
    for move in game_history:
        print(move[0], "guessed", move[1])
        if move[0] == "Player":
            if is_hit(move[1], computer_grid):
                print("Player hit a ship!")
            else:
                print("Player missed!")
        else:
            if is_hit(move[1], player_grid):
                print("Computer hit one of your ships!")
            else:
                print("Computer missed!")

    play_again = input("Do you want to play again? (y/n): ")
    if play_again.lower() != "y":
        print("Thank you for playing Battleships!")



        return

def display_game_status(player_hits, player_misses, player_ships, computer_hits, computer_misses, computer_ships):
    print("Current Game Status:")
    print("Player Hits:", player_hits)
    print("Player Misses:", player_misses)
    print("Player Remaining Ships:", player_ships)
    print("Computer Hits:", computer_hits)
    print("Computer Misses:", computer_misses)
    print("Computer Remaining Ships:", computer_ships)


def main():
    level = 1  # Default difficulty level (1: Easy, 2: Medium, 3: Hard)
    time_limits = {1: 30, 2: 20, 3: 10}  # Time limit for each difficulty level

    while True:
        main_menu()
        choice = get_user_input("Enter your choice: ", type_=int, min_=1, max_=3)

        if choice == 1:
            play_game()
        elif choice == 2:
            difficulty_menu()
            level = get_user_input("Select difficulty level: ", type_=int, min_=1, max_=3)
        elif choice == 3:
            print("Thank you for playing Battleships!")
            break

def main_menu():
    print("1. Start Game")
    print("2. Difficulty Level")
    print("3. Quit")

def difficulty_menu():
    print("1. Easy (30 seconds per turn)")
    print("2. Medium (20 seconds per turn)")
    print("3. Hard (10 seconds per turn)")

def get_user_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        if min_ is not None and ui < min_:
            print("Input must be at least {0}.".format(min_))
        elif max_ is not None and ui > max_:
            print("Input must be at most {0}.".format(max_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join(map(str, range_))))
        else:
            return ui

def main():
    size = 5  # Default grid size
    num_ships = 3  # Default number of ships
    level = 1  # Default difficulty level (1: Easy, 2: Medium, 3: Hard)
    time_limits = {1: 30, 2: 20, 3: 10}  # Time limit for each difficulty level

    while True:
        main_menu()
        choice = get_user_input("Enter your choice: ", type_=int, min_=1, max_=3)

        if choice == 1:
            play_game(size, num_ships, level, time_limits[level])
        elif choice == 2:
            difficulty_menu()
            level = get_user_input("Select difficulty level: ", type_=int, min_=1, max_=3)
        elif choice == 3:
            print("Thank you for playing Battleships!")
            break

if __name__ == "__main__":
    main()