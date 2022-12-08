from typing import Set, Tuple


def visible_from_tree(column_number: int, row_number: int):
  #Left to right
  max_height = int(rows[row_number][column_number])
  x = column_number + 1
  visible_right = 0
  while x < n_columns:
    if int(rows[row_number][x]) >= max_height:
      visible_right+=1
      break
    elif int(rows[row_number][x]) < max_height:
      x += 1
      visible_right+=1
    else:
      break

  #Right to left
  max_height = int(rows[row_number][column_number])
  x = column_number - 1
  visible_left = 0
  while x >= 0:
    if int(rows[row_number][x]) >= max_height:
      visible_left+=1
      break
    elif int(rows[row_number][x]) < max_height:
      x -= 1
      visible_left+=1
    else:
      break

  #Downwards
  max_height = int(rows[row_number][column_number])
  y = row_number + 1
  visible_down = 0
  while y < n_rows:
    if int(rows[y][column_number]) >= max_height:
      visible_down+=1
      break
    elif int(rows[y][column_number]) < max_height:
      y += 1
      visible_down+=1
    else:
      break

  #Upwards
  max_height = int(rows[row_number][column_number])
  y = row_number - 1
  visible_up = 0
  while y >= 0:
    if int(rows[y][column_number]) >= max_height:
      visible_up+=1
      break
    elif int(rows[y][column_number]) < max_height:
      y -= 1
      visible_up+=1
    else:
      break

  return visible_left*visible_right*visible_down*visible_up  


with open("Day08/data.txt") as f:
  rows = f.read().splitlines()
  n_rows = len(rows)
  n_columns = len(rows[0])

  seen: Set[Tuple[int,int]] = set()
  best_score = 0

  for row_number, row in enumerate(rows):

    for column_number in range(n_columns):
      score = visible_from_tree(column_number, row_number)
      best_score = max(best_score, score)

print(best_score)      #671160