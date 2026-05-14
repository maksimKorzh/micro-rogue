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

# Create horizontal passages
def make_horizontal_passage(x, y):
  # Remove dead ends
  step = 1
  hit_wall = False
  while x+step < COLS-1:
    if dungeon[y][x+step] == '|':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return
  
  # Avoid hitting dead a wall
  step = 1
  while x+step < COLS-1:
    if dungeon[y][x+step] == '-': return
    step += 1
    
  # Draw passage
  step = 0
  while x+step < COLS-1:
    if step == 0:
      dungeon[y][x+step] = '+'
      step += 1
    elif dungeon[y][x+step] == '|':
      dungeon[y][x+step] = '+'
      break
    dungeon[y][x+step] = '#'
    step += 1

# Create vertical passages
def make_vertical_passage(x, y):
  # Remove dead ends|
  step = 1
  hit_wall = False
  while y+step < ROWS-1:
    if dungeon[y+step][x] == '-':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return

  # Avoid hitting a dead wall  
  step = 1
  while y+step < ROWS-1:
    if dungeon[y+step][x] == '|': return
    step += 1

  # Draw passage
  step = 0
  while y+step < ROWS-1:
    if step == 0:
      dungeon[y+step][x] = '+'
      step += 1
    elif dungeon[y+step][x] == '-':
      dungeon[y+step][x] = '+'
      break
    dungeon[y+step][x] = '#'
    step += 1

# Create new level
def make_level():
  # Clear dungeon
  for row in range(ROWS):
    for col in range(COLS):
      dungeon[row][col] = ' '

  # Room doors
  doors_v = []
  doors_h = []

  # Generate random rooms
  for r in range(3):
    for c in range(3):
      w = randrange(10, 20)
      h = randrange(5, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      doors_v.append([x+w-1, y+int(h/2)])
      doors_h.append([x+int(w/2), y+h-1])
      make_room(x, y, w, h)
  
  # Generate passage
  for door in doors_v: make_horizontal_passage(door[0], door[1])
  for door in doors_h: make_vertical_passage(door[0], door[1])

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

while True:
  make_level()
  print_level()
  input()
