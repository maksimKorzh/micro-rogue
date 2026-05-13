import sys
import curses
from random import randrange, choice

ROWS = 23
COLS = 79

dungeon = [[' ']*COLS for i in range(ROWS)]

player_x = 0
player_y = 0

def populate_dungeon():
  global player_x, player_y
  floor_tiles = []
  for row in range(ROWS):
    for col in range(COLS):
      if dungeon[row][col] == '.':
        floor_tiles.append([col, row])
  player_pos = choice(floor_tiles)
  player_x = player_pos[0]
  player_y = player_pos[1]

def make_room(x, y, w, h):
  for row in range(y, y + h):
    for col in range(x, x + w):
      if row == y or row == y+h-1: dungeon[row][col] = '-'
      elif col == x or col == x+w-1: dungeon[row][col] = '|'
      else: dungeon[row][col] = '.'

def make_horizontal_passage(x, y):
  step = 1
  hit_wall = False
  while(x+step < COLS):
    if dungeon[y][x+step] == '|':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return
  step = 1
  while(x+step < COLS):
    if dungeon[y][x+step] == '-': return
    step += 1
  step = 0
  while(x+step < COLS):
    if step == 0:
      dungeon[y][x+step] = '+'
      step += 1
    if dungeon[y][x+step] == '|':
      dungeon[y][x+step] = '+'
      break
    dungeon[y][x+step] = '#'
    step += 1

def make_vertical_passage(x, y):
  step = 1
  hit_wall = False
  while(y+step < ROWS):
    if dungeon[y+step][x] == '-':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return
  step = 1
  while(y+step < ROWS):
    if dungeon[y+step][x] == '|': return
    step += 1
  step = 0
  while(y+step < ROWS):
    if step == 0:
      dungeon[y+step][x] = '+'
      step += 1
    if dungeon[y+step][x] == '-':
      dungeon[y+step][x] = '+'
      break
    dungeon[y+step][x] = '#'
    step += 1

def make_level():

  #for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  #dungeon.append([' ']*COLS)
  #for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  #dungeon.append([' ']*COLS)
  #for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  
  for row in range(ROWS):
    for col in range(COLS):
      dungeon[row][col] = ' '

  doors_x = []
  doors_y = []
  for r in range(3):
    for c in range(3):
      w = randrange(6, 20)
      h = randrange(5, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      px = randrange(x+1, x+w-1)
      py = randrange(y+1, y+h-1)
      doors_x.append([x+w-1, py])
      doors_y.append([px, y+h-1])
      make_room(x, y, w, h)
  
  for door in doors_x: make_horizontal_passage(door[0], door[1])
  for door in doors_y: make_vertical_passage(door[0], door[1])
  populate_dungeon()

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

def render_level():
  screen.move(0, 0)
  for row in range(ROWS):
    for col in range(COLS):
      screen.addch(row, col, dungeon[row][col])
    screen.clrtoeol()
    screen.addch('\n')
  curses.curs_set(0)
  screen.addch(player_y, player_x, '@')
  screen.move(player_y, player_x)
  curses.curs_set(1)
  screen.refresh()

def read_keys():
  global player_x, player_y
  ch = -1
  while (ch == -1): ch = screen.getch()
  if ch == ord('h'):
    if dungeon[player_y][player_x-1] not in '-| ':
      player_x -= 1
  elif ch == ord('j'):
    if dungeon[player_y+1][player_x] not in '-| ':
      player_y += 1
  elif ch == ord('k'):
    if dungeon[player_y-1][player_x] not in '-| ':
      player_y -= 1
  elif ch == ord('l'):
    if dungeon[player_y][player_x+1] not in '-| ':
      player_x += 1
  elif ch == ord('q'):
    curses.endwin()
    sys.exit()



screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()



make_level()

while True:
  render_level()
  read_keys()
