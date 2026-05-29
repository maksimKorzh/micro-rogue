#########################
#
#        PACKAGES
#
#########################

import sys
import json
import curses
import string
from random import randrange, choice

#########################
#
#       CONSTANTS
#
#########################

ROWS = 23
COLS = 80

#########################
#
#        VARIABLES
#
#########################

amulet_level = 26
dungeon = [[' ']*COLS for i in range(ROWS)]
visited_tiles = []
revealed_traps = []
dungeon_level = 1
dark_rooms = False
monsters = string.ascii_uppercase
player_x = 0
player_y = 0
player_hp = 12
player_food = 1200
player_steps = 0
player_armor = 1
player_weapon = 1
player_amulet = 0

#########################
#
#       FUNCTIONS
#
#########################

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
  # Globals to change
  global player_x, player_y
  
  # Place stairs
  stair_pos = choice(get_floor_tiles())
  dungeon[stair_pos[1]][stair_pos[0]] = '%'
  
  # Place items
  weapons = randrange(0, 2)
  for i in range(weapons):
    weapon_pos = choice(get_floor_tiles())
    dungeon[weapon_pos[1]][weapon_pos[0]] = ')'
  armors = randrange(0, 2)
  for i in range(armors):
    armor_pos = choice(get_floor_tiles())
    dungeon[armor_pos[1]][armor_pos[0]] = ']'
  foods = randrange(1,4)
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

  # Place traps
  traps = randrange(0, int(dungeon_level/4)+1)
  for i in range(traps):
    trap_pos = choice(get_floor_tiles())
    dungeon[trap_pos[1]][trap_pos[0]] = '^'

  # Place Amulet of Yendor
  if dungeon_level == amulet_level:
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
  # Globals to change
  global visited_tiles, revealed_traps
  
  # Clear visited tiles
  visited_tiles = []
  
  # Clear revealed traps
  revealed_traps = []

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

# Render level to screen
def render_level():
  # Avoid glitches
  curses.curs_set(0)
  screen.move(0, 0)
  screen.clrtoeol()
  
  # Render dungeon
  for row in range(ROWS):
    for col in range(COLS):
      if dark_rooms:
        if [col, row] in visited_tiles:
          if dungeon[row][col] == '^':
            if [col, row] in revealed_traps: screen.addch(row, col, '^')
            else: screen.addch(row, col, '.')
          else: screen.addch(row, col, dungeon[row][col])
        elif row in range(player_y-1, player_y+2) and col in range(player_x-1, player_x+2):
          if dungeon[row][col] == '^': screen.addch(row, col, '.')
          else: screen.addch(row, col, dungeon[row][col])
          visited_tiles.append([col, row])
        else: screen.addch(row, col, ' ')
      else:
        if dungeon[row][col] == '^':
          if [col, row] in revealed_traps: screen.addch(row, col, '^')
          else: screen.addch(row, col, '.')
        else: screen.addch(row, col, dungeon[row][col])

  # Render status line
  screen.addstr(23, 0, f'Level: {dungeon_level}  HP: {player_hp}  Attack: {player_weapon}  Defense: {player_armor}  Amulet of Yendor({amulet_level}): {player_amulet}       Food: {player_food}')
  screen.clrtoeol()
  
  # Render player
  screen.addch(player_y, player_x, '@')
  screen.move(player_y, player_x)
  
  # Update screen
  curses.curs_set(1)
  screen.refresh()

# Take user input
def read_key():
  # Read key from keyboard
  ch = -1
  while ch == -1: ch = screen.getch()
  
  # Run or move
  if ch == ord('H'): run(0, -1, ord('h'))
  elif ch == ord('J'): run(1, 0, ord('j'))
  elif ch == ord('K'): run(-1, 0, ord('k'))
  elif ch == ord('L'): run(0, 1, ord('l'))
  elif ch == ord('Y'): run(-1, -1, ord('y'))
  elif ch == ord('U'): run(-1, 1, ord('u'))
  elif ch == ord('B'): run(1, -1, ord('b'))
  elif ch == ord('N'): run(1, 1, ord('n'))
  else: move(ch)

# Run rogue
def run(y, x, ch):
  while dungeon[player_y+y][player_x+x] in '.#^':
    move(ch)
    render_level()
    if dungeon[player_y][player_x] == '^': break

# Move rogue
def move(ch):
  # Globals to change
  global player_x, player_y, player_hp, player_steps, player_food
  
  # HP restore logic, food consumption
  if ch in [
    ord('h'), ord('j'), ord('k'), ord('l'),
    ord('y'), ord('u'), ord('b'), ord('n'),
  ]:
    player_steps += 1
    if not player_steps % (30-dungeon_level): player_hp += 1
    player_food -= 1
    
  # Orthogonal motion control
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
  elif ch == ord('w'):
    for i in range(50):
      player_steps += 1
      if not player_steps % (30-dungeon_level): player_hp += 1
      player_food -= 1

  # Diagonal motion control
  if dungeon[player_y][player_x] != '+':
    if ch == ord('y'):
      if dungeon[player_y-1][player_x-1] not in '-|+ ':
        player_x -= 1
        player_y -= 1
    elif ch == ord('b'):
      if dungeon[player_y+1][player_x-1] not in '-|+ ':
        player_x -=1
        player_y += 1
    if ch == ord('u'):
      if dungeon[player_y-1][player_x+1] not in '-|+ ':
        player_x += 1
        player_y -= 1
    if ch == ord('n'):
      if dungeon[player_y+1][player_x+1] not in '-|+ ':
        player_x += 1
        player_y += 1

  # Escape condition
  if ch == ord('q'):
    curses.endwin()
    sys.exit()
  elif ch == ord('S'):
    save()
    curses.endwin()
    print('Game saved to "rogue.json"')
    sys.exit()

# Figth monsters
def battle():
  # Globals to change
  global player_hp, player_weapon, player_armor
  
  # Init monster stats
  monster = dungeon[player_y][player_x]
  monster_hp = (ord(monster) - ord('A')+1)*2
  monster_damage = monster_hp
  
  # Fighting loop
  while player_hp > 0:
    # Player hits monster
    damage = randrange(player_weapon+1)
    monster_hp -= damage
    screen.addstr(0, 0, f'You hit {monster}({monster_hp}) by {damage} point(s), press "f" to fight')
    screen.clrtoeol()
    screen.refresh()
    
    # Player kills monster
    if monster_hp <= 0:
      dungeon[player_y][player_x] = '.'
      screen.addstr(0, 0, f'You killed {monster}, press "f" to finish the fight')
      screen.clrtoeol()
      screen.refresh()
      if player_weapon < dungeon_level+10: player_weapon += randrange(0, 2) + monsters.index(monster)
      if player_armor < dungeon_level+10: player_armor += randrange(0, 2) + monsters.index(monster)
    
    # Wait for user input
    ch = -1
    while ch == -1:
      ch = screen.getch()
      if ch != ord('f'): ch = -1
    if monster_hp <= 0: break
    
    # Monster hits player
    damage = max(0, randrange(monster_damage)*2 - player_armor)
    player_hp -= damage
    render_level()
    screen.addstr(0, 0, f'{monster}({monster_hp}) hits you by {damage} point(s), press "f" to fight, "e" to escape')
    screen.clrtoeol()
    screen.refresh()
    
    # Wait for user input
    ch = -1
    while ch == -1:
      ch = screen.getch()
      if ch == ord('e'): return
      elif ch != ord('f'): ch = -1

# Interact with the dungeon
def take_action():
  # Globals to change
  global player_amulet, player_weapon, player_armor, player_food, player_hp
  global dungeon_level, revealed_traps, dark_rooms
  
  # Change dungeon level
  if dungeon[player_y][player_x] == '%':
    dungeon_level = dungeon_level+1 if not player_amulet else dungeon_level-1
    if not dungeon_level:
      curses.endwin()
      print('You won!')
      sys.exit()
    else:
      if dungeon_level > int(amulet_level/2): dark_rooms = True
      else: dark_rooms = False
      make_level()
  elif dungeon[player_y][player_x] == '!': player_amulet = 1
  elif dungeon[player_y][player_x] == ')': player_weapon += 1
  elif dungeon[player_y][player_x] == ']': player_armor += 1
  elif dungeon[player_y][player_x] == '*': player_food += int(randrange(100, len(get_floor_tiles()))/2)
  
  # Fight monster
  if dungeon[player_y][player_x] in monsters: battle()
  
  # Remove picked item
  if dungeon[player_y][player_x] in '!)]*': dungeon[player_y][player_x] = '.'
  
  # Got into trap
  if dungeon[player_y][player_x] == '^':
    damage = randrange(5, 10+int(dungeon_level/2))
    player_hp -= damage
    revealed_traps.append([player_x, player_y])
    screen.addstr(0, 0, f'You got into trap! Your HP decreases by {damage} points, press any key to continue')
    screen.clrtoeol()
    screen.refresh()
    
    # Wait for user input
    ch = -1
    while ch == -1:
      ch = screen.getch()

  # Death condition
  if player_hp <= 0 or player_food <= 0:
    curses.endwin()
    print('You died!')
    sys.exit()
  
# Save game
def save():
  with open('rogue.json', 'w') as f:
    f.write(json.dumps({
      'amulet_level': amulet_level,
      'dungeon': json.dumps(dungeon),
      'visited_tiles': json.dumps(visited_tiles),
      'revealed_traps': json.dumps(revealed_traps),
      'dungeon_level': dungeon_level,
      'dark_rooms': dark_rooms,
      'player_x': player_x,
      'player_y': player_y,
      'player_hp': player_hp,
      'player_food': player_food,
      'player_steps': player_steps,
      'player_armor': player_armor,
      'player_weapon': player_weapon,
      'player_amulet': player_amulet
    }, indent=2))

# Load game
def load():
  global amulet_level, dungeon, visited_tiles, revealed_traps, dungeon_level, dark_rooms
  global player_x, player_y, player_hp, player_food, player_steps
  global player_armor, player_weapon, player_amulet
  try:
    with open('rogue.json') as f:
      game = json.loads(f.read())
      amulet_level = game['amulet_level']
      dungeon = json.loads(game['dungeon'])
      visited_tiles = json.loads(game['visited_tiles'])
      revealed_traps = json.loads(game['revealed_traps'])
      dungeon_level = game['dungeon_level']
      dark_rooms = game['dark_rooms']
      player_x = game['player_x']
      player_y = game['player_y']
      player_hp = game['player_hp']
      player_food = game['player_food']
      player_steps = game['player_food']
      player_armor = game['player_armor']
      player_weapon = game['player_weapon']
      player_amulet = game['player_amulet']
  except: raise Exception

#########################
#
#          MAIN
#
#########################

# Load saved game or set up difficulty
try:
  load()
  print('Loaded saved game')
except:
  try:
    amulet_level = int(input('Amulet Of Yendor Level (1-26) > '))
    if amulet_level not in range(1,27):
      amulet_level = 26
      print('Amulet Of Yendor is placed on level 26')
      input()
  except:
    print('Amulet Of Yendor is placed on level 26')
    input()

  # Make first level
  make_level()

# Init curses
screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()


# Game loop
while True:
  render_level()
  read_key()
  take_action()
