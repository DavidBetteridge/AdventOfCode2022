

from typing import Set, Tuple


with open("Day09/data.txt") as f:
  tail_position = (0,0)
  head_position = (0,0)
  visited: Set[Tuple[int,int]] = set()
  for move in f:
    x_offset = 0
    y_offset = 0
    match move.strip().split():
      case "R", distance:
        x_offset=1
      case "U", distance:
        y_offset=-1
      case "D", distance:
        y_offset=1
      case "L", distance:
        x_offset=-1
      case _:
        raise Exception("")

    for _ in range(int(distance)):
      head_position = (head_position[0]+x_offset, head_position[1]+y_offset)

      is_touching = abs(head_position[0] - tail_position[0]) <= 1 and \
                    abs(head_position[1] - tail_position[1]) <= 1

      if not is_touching:
        if head_position[0] == tail_position[0]:
          # In the same column, so need to adjust the row
          y_adjustment = 1 if head_position[1] > tail_position[1] else -1
          tail_position = (tail_position[0], tail_position[1]+y_adjustment)
        elif head_position[1] == tail_position[1]:
          # In the same row, so need to adjust the column
          x_adjustment = 1 if head_position[0] > tail_position[0] else -1
          tail_position = (tail_position[0]+x_adjustment, tail_position[1])
        else:
          # We need to adjust both
          y_adjustment = 1 if head_position[1] > tail_position[1] else -1
          x_adjustment = 1 if head_position[0] > tail_position[0] else -1
          tail_position = (tail_position[0]+x_adjustment, tail_position[1]+y_adjustment)
      visited.add(tail_position)

  print(len(visited))