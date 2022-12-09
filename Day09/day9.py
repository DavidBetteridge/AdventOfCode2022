

from typing import Set, Tuple, List

def catch_up(head_position:Tuple[int,int], tail_position:Tuple[int,int]):
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
  return tail_position

def solve(rope_length: int) -> int:
  with open("Day09/data.txt") as f:
    
    rope: List[Tuple[int,int]] = []
    for _ in range(rope_length):
      rope.append((0,0))
    
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
        # Move the head of the rope
        rope[0] = (rope[0][0]+x_offset, rope[0][1]+y_offset)
        
        # Let the tails catch up
        for i in range(rope_length-1):
          rope[i+1] = catch_up(rope[i], rope[i+1])

        visited.add(rope[-1])
    return len(visited)


part1 = solve(2)
assert part1 == 5710

part2 = solve(10)
assert part2 == 2259

print(part1, part2)