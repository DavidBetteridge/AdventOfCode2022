from collections import defaultdict
from typing import Dict, List, Set, Tuple


X = int
Y = int

def bounding_box(elves: Set[Tuple[X,Y]]):
  left = min([x for x,y in elves])
  right = max([x for x,y in elves])
  top = min([y for x,y in elves])
  bottom = max([y for x,y in elves])
  return (left,top), (right,bottom)

def display(elves: Set[Tuple[X,Y]]):
  print()
  print()
  (left,top), (right,bottom) = bounding_box(elves)
  for r in range(top-1, bottom+2):
    for c in range(left-2, right+2):
      if (c,r) in elves:
        print("#", end="")
      else:
        print(".", end="")
    print("")

with open("Day23/data.txt") as f:
  rows = f.read().splitlines()

  # Elves is a set of tuples containing all the cells which contain an Elf.
  elves: Set[Tuple[X,Y]] = set()

  for row_number, row in enumerate(rows):
    for column_number, cell in enumerate(row):
      if cell == '#':
        elves.add((column_number, row_number))


display(elves)

north = [(-1,-1),(0,-1),(1,-1)]
south = [(-1, 1),(0, 1),(1, 1)]
west  = [(-1, -1),(-1, 0),(-1, 1)]
east  = [( 1, -1),( 1, 0),( 1, 1)]
directions = [north, south, west, east]
all_directions = [(-1,-1),(0,-1),(1,-1),
                  (-1,0),   (1,0),
                  (-1,1),(0,1),(1,1)]

round = 0
moved = True
while moved:

  proposed: Dict[Tuple[X,Y],List[Tuple[X,Y]]] = defaultdict(list)  #TO/FROM

  for elf_x, elf_y in elves:

    if any((elf_x+offset_x,elf_y+offset_y) in elves for offset_x, offset_y in all_directions):
      for direction_number in range(4):
        direction_to_test = directions[(round + direction_number) % 4]
        ok = all((elf_x+offset_x,elf_y+offset_y) not in elves for offset_x, offset_y in direction_to_test)
        if ok:
          offset_x, offset_y = direction_to_test[1]
          proposed[(elf_x+offset_x, elf_y+offset_y)].append((elf_x, elf_y)) 
          break
      else:
        proposed[(elf_x, elf_y)].append((elf_x, elf_y))
    else:
      proposed[(elf_x, elf_y)].append((elf_x, elf_y))         

  elves.clear()

  moved = False
  for to_, from_ in proposed.items():
    if len(from_) == 1:
      elves.add(to_)
      if not moved:
        moved = (to_ != from_[0])
    else:
      for f in from_:
        elves.add(f)

  round += 1
  print(round)  
