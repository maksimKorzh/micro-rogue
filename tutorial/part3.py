# Packages
import string
from random import randrange, choice

# Constants
ROWS = 23
COLS = 79
AMULET_LEVEL = 1

# Variables
dungeon = [[' ']*COLS for i in range(ROWS)]
dungeon_level = 1
monsters = string.ascii_uppercase
player_x = 0
player_y = 0

# Functions

# Find all empty floor tiles
def get_floor_tiles():
  floor_tiles = []
  for row in range(ROWS):
    for col in range(COLS):
      if dungeon[row][col] == '.':
        floor_tiles.append([col, row])
  return floor_tiles

# Find all door blocking floor tiles
def get_blocking_tiles():
  floor_tiles = []
  for row in range(ROWS):
    for col in range(COLS):
      if dungeon[row][col] == '.':
        try:
          if dungeon[row+1][col] == '+' or \
             dungeon[row-1][col] == '+' or \
             dungeon[row][col+1] == '+' or \
             dungeon[row][col-1] == '+':
            floor_tiles.append([col, row])
        except: pass
  return floor_tiles

# Fill the dungeon with stairs, items and monsters
def fill_dungeon():
  # Place stairs
  stair_pos = choice(get_floor_tiles())
  dungeon[stair_pos[1]][stair_pos[0]] = '%'
  
  # Place items
  weapons = randrange(0, 3)
  for i in range(weapons):
    weapon_pos = choice(get_floor_tiles())
    dungeon[weapon_pos[1]][weapon_pos[0]] = ')'
  armors = randrange(0, 3)
  for i in range(armors):
    armor_pos = choice(get_floor_tiles())
    dungeon[armor_pos[1]][armor_pos[0]] = ']'
  foods = randrange(0,2)
  for i in range(foods):
    food_pos = choice(get_floor_tiles())
    dungeon[food_pos[1]][food_pos[0]] = '*'
  
  # Place monsters
  idle_monsters = randrange(6, 12+dungeon_level)
  guard_monsters = randrange(2, min(12, 5+int(dungeon_level/2)))
  for i in range(idle_monsters):
    monster = choice(monsters[dungeon_level-1: dungeon_level+3])
    monster_pos = choice(get_floor_tiles())
    dungeon[monster_pos[1]][monster_pos[0]] = monster
  for i in range(guard_monsters):
    monster = choice(monsters[dungeon_level-1: dungeon_level+3])
    monster_pos = choice(get_blocking_tiles())
    dungeon[monster_pos[1]][monster_pos[0]] = monster

  # Place Amulet of Yendor
  if dungeon_level == AMULET_LEVEL:
    amulet_pos = choice(get_floor_tiles())
    dungeon[amulet_pos[1]][amulet_pos[0]] = '!'
  
  # Place player
  player_pos = choice(get_floor_tiles())
  player_x = player_pos[0]
  player_y = player_pos[1]

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
  
  # Fill the dungeon
  fill_dungeon()

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

while True:
  make_level()
  print_level()
  input()
