from random import randrange

dungeon = []

def make_room(x, y, w, h):
  for row in range(y, y + h):
    for col in range(x, x + w):
      if row == y or row == y+h-1: dungeon[row][col] = '-'
      elif col == x or col == x+w-1: dungeon[row][col] = '|'
      else: dungeon[row][col] = '.'

def make_level():
  # Init empty dungeon
  for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  dungeon.append([' ']*80)
  for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)
  dungeon.append([' ']*80)
  for i in range(7): dungeon.append(['o']*26 + [' '] + ['o']*26 + [' '] + ['o']*26)

  for r in range(3):
    for c in range(3):
      w = randrange(4, 20)
      h = randrange(4, 7)
      x = randrange(c*27, c*27+(26-w))
      y = randrange(r*8, r*8+(7-h))
      make_room(x, y, w, h)

def print_level():
  for row in dungeon:
    for col in row:
      print(col, end='')
    print()

make_level()
print_level()
