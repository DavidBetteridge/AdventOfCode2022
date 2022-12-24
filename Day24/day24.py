from collections import defaultdict
from typing import Dict, List, Set, Tuple
from functools import lru_cache

with open(r"C:\Personal\AdventOfCode2022\Day24\data.txt") as f:
  lines = f.read().splitlines()[1:-1]

  up_down: Dict[int, Dict[int, int]] = defaultdict(dict)
  left_right: Dict[int, Dict[int, int]] = defaultdict(dict)

  n_columns = len(lines[0])-2
  n_rows = len(lines)
  
  for row_number, row in enumerate(lines):
    for column_number, cell in enumerate(row[1:-1]):
      if cell == "^":
        up_down[column_number][row_number] = -1
      elif cell == "v":
        up_down[column_number][row_number] = 1
      elif cell == "<":
        left_right[row_number][column_number] = -1
      elif cell == ">":
        left_right[row_number][column_number] = +1

  @lru_cache(maxsize=None)
  def row_at_time_t(row_number: int, t: int):
    row = [False] * n_columns
    for column_number, dir in left_right[row_number].items():
      row[(column_number + (t * dir)) % n_columns] = True
    return row

  @lru_cache(maxsize=None)
  def column_at_time_t(column_number: int, t: int):
    column = [False] * n_rows
    for row_number, dir in up_down[column_number].items():
      column[(row_number + (t * dir)) % n_rows] = True
    return column

  def print_at_time(t):
    for r in range(n_rows):
      for c in range(n_columns):
        if row_at_time_t(r,t)[c]:
          print("-",end="")
        elif column_at_time_t(c,t)[r]:
          print("|",end="")
        else:
          print(".",end="")
      print("")

X = int
Y = int
TIME = int

queue: List[Tuple[X, Y, TIME]] = [(0,-1,0)]
seen: Set[Tuple[X, Y, TIME]] = set()
dirs = [(0,0),(-1,0),(1,0),(0,-1),(0,1)]

big_t = 0
while len(queue) > 0:
  x,y,t = queue.pop(0)
  if (x,y,t) not in seen:
    seen.add((x,y,t))

    if t > big_t:
      print("time=", t, "queue=", len(queue))
      big_t = t

    if y == (n_rows-1) and x == (n_columns-1):
      print("Solution at time", t+1) 
      quit()

    for x_offset, y_offset in dirs:
      new_x = x + x_offset
      new_y = y + y_offset
      if (0 <= new_x < n_columns) and (0 <= new_y < n_rows):
          if (not row_at_time_t(new_y,t+1)[new_x]) and \
            (not column_at_time_t(new_x,t+1)[new_y]):
              queue.append((new_x, new_y, t+1))
  
  

