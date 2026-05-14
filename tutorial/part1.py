# Packages
from random import randrange

# Constants
ROWS = 23
COLS = 79

# Variables
dungeon = [[' ']*COLS for i in range(ROWS)]

# Functions

# Create new room
def make_room(x, y, w, h):
  for row in range(y, y+h):
    for col in range(x, x+w):
      if row == y or row == y+h-1: dungeon[row][col] = '-'
      elif col == x or col == x+w-1: dungeon[row][col] = '|'
      else: dungeon[row][col] = '.'

# Create new level
def make_level():
  # Clear dungeon
  for row in range(ROWS):
    for col in range(COLS):
      dungeon[row][col] = ' '

  # Generate random rooms
  for r in range(3):
    for c in range(3):
      w = randrange(10, 20)
      h = randrange(5, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      make_room(x, y, w, h)

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

while True:
  make_level()
  print_level()
  input()
