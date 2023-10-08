# Import the random module to generate random
import random


# Function to create a grid of given size filled with 'o'
def create_grid(size):
    return [['o'] * size for _ in range(size)]


# Function to print the grid in a nice format
def print_grid(grid):
    size = len(grid)
    print("  " + " ".join([chr(65+i) for i in range(size)])) # Print column headers (A, B, C, ...)
    print("  " + "-" * (2*size+1)) # print line separator


