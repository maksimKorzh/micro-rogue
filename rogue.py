import sys
import string
import curses
from random import randrange, choice

ROWS = 23
COLS = 79

AMULET_LEVEL = 3

visited = []
dungeon = [[' ']*COLS for i in range(ROWS)]
dungeon_level = 1
monsters = string.ascii_uppercase

player_x = 0
player_y = 0
player_steps = 0
player_hp = 12
player_weapon = 1
player_armor = 1
player_amulet = 0

def battle():
  global player_hp
  monster = dungeon[player_y][player_x]
  monster_hp = (ord(monster) - ord('A') + 1)*2
  monster_damage = monster_hp
  while player_hp > 0:
    damage = randrange(player_weapon+1)
    monster_hp -= damage
    screen.addstr(0, 0, f'You deal {damage} points of damage to {monster}({monster_hp})'); screen.clrtoeol()
    screen.refresh()
    if monster_hp <= 0:
      dungeon[player_y][player_x] = '.'
      screen.addstr(0, 0, f'You killed {monster}({monster_hp})'); screen.clrtoeol()
      screen.refresh()
    ch = -1
    while ch == -1: ch = screen.getch()
    if monster_hp <= 0: break
    damage = max(0, randrange(monster_damage)*2 - player_armor)
    player_hp -= damage
    render_level()
    screen.addstr(0, 0, f'{monster} deals {damage} points of damage to you'); screen.clrtoeol()
    screen.refresh()
    ch = -1
    while ch == -1: ch = screen.getch()

def get_floor_tiles():
  floor_tiles = []
  for row in range(ROWS):
    for col in range(COLS):
      if dungeon[row][col] == '.':
        floor_tiles.append([col, row])
  return floor_tiles

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

def populate_dungeon():
  global player_x, player_y
  stairs_pos = choice(get_floor_tiles())
  dungeon[stairs_pos[1]][stairs_pos[0]] = '%'
  monster_idle = randrange(6, 12+dungeon_level)
  monster_guard = randrange(2, min(12, 5+int(dungeon_level/2)))
  for i in range(monster_idle):
    monster = choice(monsters[dungeon_level-1: dungeon_level+3])
    monster_pos = choice(get_floor_tiles())
    dungeon[monster_pos[1]][monster_pos[0]] = monster
  for i in range(monster_guard):
    monster = choice(monsters[dungeon_level-1: dungeon_level+3])
    monster_pos = choice(get_blocking_tiles())
    dungeon[monster_pos[1]][monster_pos[0]] = monster
  items = randrange(2, 6)
  for i in range(items):
    weapon_pos = choice(get_floor_tiles())
    dungeon[weapon_pos[1]][weapon_pos[0]] = ')'
  for i in range(items):
    armor_pos = choice(get_floor_tiles())
    dungeon[armor_pos[1]][armor_pos[0]] = ']'
  for i in range(items):
    food_pos = choice(get_floor_tiles())
    dungeon[food_pos[1]][food_pos[0]] = '*'
  if dungeon_level == AMULET_LEVEL:
    amulet_pos = choice(get_floor_tiles())
    dungeon[amulet_pos[1]][amulet_pos[0]] = '!'
  player_pos = choice(get_floor_tiles())
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
  global visited
  visited = []
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
      w = randrange(10, 20)
      h = randrange(5, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      doors_x.append([x+w-1, y+int(h/2)])
      doors_y.append([x+int(w/2), y+h-1])
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
      if [col, row] in visited: screen.addch(row, col, dungeon[row][col])
      elif row in range(player_y-1, player_y+2) and col in range(player_x-1, player_x+2):
        screen.addch(row, col, dungeon[row][col])
        visited.append([col, row])
      else: screen.addch(row, col, ' ')
    screen.clrtoeol()
    screen.addch('\n')
  screen.addstr(23, 0, f'Level: {dungeon_level}  HP: {player_hp}  Weapon: {player_weapon}  Armor: {player_armor}  Amulet Of Yendor: {player_amulet}')
  screen.clrtoeol()
  curses.curs_set(0)
  screen.addch(player_y, player_x, '@')
  screen.move(player_y, player_x)
  curses.curs_set(1)
  screen.refresh()

def read_keys():
  global player_x, player_y, player_steps, player_hp
  ch = -1
  while ch == -1: ch = screen.getch()
  if ch in [ord('h'), ord('j'), ord('k'), ord('l')]:
    player_steps += 1
    if not player_steps % 128: player_hp -= 1
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

def take_action():
  global dungeon_level, player_amulet, player_weapon, player_armor, player_hp
  if dungeon[player_y][player_x] == '%':
    dungeon_level = dungeon_level+1 if not player_amulet else dungeon_level-1
    if not dungeon_level:
      curses.endwin()
      print('You won!')
      sys.exit()
    else: make_level()
  elif dungeon[player_y][player_x] == '!': player_amulet = 1
  elif dungeon[player_y][player_x] == ')': player_weapon += 1
  elif dungeon[player_y][player_x] == ']': player_armor += 1
  elif dungeon[player_y][player_x] == '*': player_hp += 6
  elif dungeon[player_y][player_x] in monsters: battle()
  if dungeon[player_y][player_x] in '!)]*': dungeon[player_y][player_x] = '.'
  if player_hp <= 0:
    curses.endwin()
    print('You died!')
    sys.exit()  

#while True:
#  make_level()
#  print_level()
#  input()
#
#sys.exit()

screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()


make_level()
#print_level()

while True:
  render_level()
  read_keys()
  take_action()
