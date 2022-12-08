from typing import Set, Tuple


with open("Day08/data.txt") as f:
  rows = f.read().splitlines()
  n_rows = len(rows)
  n_columns = len(rows[0])

  seen: Set[Tuple[int,int]] = set()
  
  for row_number, row in enumerate(rows):

    # Left to Right
    min_height = -1
    for column_number, tree in enumerate(row):
      if int(tree) == min_height:
        pass
      elif int(tree) > min_height:
        seen.add((column_number, row_number))
        min_height = int(tree)

    # Right to Left
    min_height = -1
    for column_number in range(n_columns-1, 0, -1):
      tree = row[column_number]
      if int(tree) == min_height:
        pass
      elif int(tree) > min_height:
        seen.add((column_number, row_number))
        min_height = int(tree)

  for column_number in range(n_columns):

    # Top to Bottom
    min_height = -1
    for row_number in range(n_rows):
      tree = rows[row_number][column_number]
      if int(tree) == min_height:
        pass
      elif int(tree) > min_height:
        seen.add((column_number, row_number))
        min_height = int(tree)

    # Bottom to Top
    min_height = -1
    for row_number in range(n_rows-1,0,-1):
      tree = rows[row_number][column_number]
      if int(tree) == min_height:
        pass
      elif int(tree) > min_height:
        seen.add((column_number, row_number))
        min_height = int(tree)

  part1 = len(seen)
  assert part1 == 1763
  print(1763) 