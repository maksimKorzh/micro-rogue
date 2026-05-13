from random import randrange

dungeon = [[' ']*80 for i in range(23)]

def make_room(x, y, w, h):
  for row in range(y, y + h):
    for col in range(x, x + w):
      if row == y or row == y+h-1: dungeon[row][col] = '-'
      elif col == x or col == x+w-1: dungeon[row][col] = '|'
      else: dungeon[row][col] = '.'

def make_horizontal_passage(x, y):
  step = 1
  hit_wall = False
  while(x+step < 80):
    if dungeon[y][x+step] == '|':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return
  step = 1
  while(x+step < 80):
    if dungeon[y][x+step] == '-': return
    step += 1
  step = 0
  while(x+step < 80):
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
  while(y+step < 23):
    if dungeon[y+step][x] == '-':
      hit_wall = True
      break
    step += 1
  if not hit_wall: return
  step = 1
  while(y+step < 23):
    if dungeon[y+step][x] == '|': return
    step += 1
  step = 0
  while(y+step < 23):
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
  #dungeon.append([' ']*80)
  #for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  #dungeon.append([' ']*80)
  #for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  
  for row in range(23):
    for col in range(80):
      dungeon[row][col] = ' '

  doors_x = []
  doors_y = []
  for r in range(3):
    for c in range(3):
      w = randrange(4, 20)
      h = randrange(4, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      px = randrange(x+1, x+w-1)
      py = randrange(y+1, y+h-1)
      doors_x.append([x+w-1, py])
      doors_y.append([px, y+h-1])
      make_room(x, y, w, h)
  
  for door in doors_x: make_horizontal_passage(door[0], door[1])
  for door in doors_y: make_vertical_passage(door[0], door[1])

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

make_level()
print_level()
