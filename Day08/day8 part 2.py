from itertools import product

with open("Day08/data.txt") as f:
  trees = f.read().splitlines()
  n_rows = len(trees)
  n_columns = len(trees[0])

def visible_from_tree(column_number: int, row_number: int):
  score = 1
  max_height = int(trees[row_number][column_number])
  for x_offset, y_offset in [(1,0), (-1,0), (0,-1), (0,1)]:
    x = column_number + x_offset
    y = row_number + y_offset
    num_visible = 0
    view_blocked = False
    while (0 <= x < n_columns) and (0 <= y < n_rows) and not view_blocked:
      num_visible+=1
      if int(trees[y][x]) >= max_height:
        view_blocked = True
      x += x_offset
      y += y_offset
    score *= num_visible
  return score

part2_score = max([visible_from_tree(column_number, row_number)
                    for row_number, column_number
                    in product(range(n_rows), range(n_columns))])
assert part2_score == 671160