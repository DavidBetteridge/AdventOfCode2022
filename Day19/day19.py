from typing import  List, Tuple
from functools import lru_cache


def parse_line(line: str) -> Tuple[int,Tuple[Tuple[int,int,int,int]]]:
  bp, robots = line.split(":")
  bp_number = int(bp[9:])

  requirements: List[Tuple[int,int,int,int]] = []
  for _ in range(4):
    requirements.append((0,0,0,0))

  for robot in robots.strip().split("."):
    if robot != "":
      lhs, costs = robot.strip()[4:].split(" robot costs ")
      robot_type = robot_types[lhs.strip()]
      for cost in costs.split(" and "):
        qty, src_type = cost.split(" ")
        value = requirements[robot_type]
        if src_type == "ore":
          requirements[robot_type] = (int(qty),value[1],value[2],value[3])
        elif src_type == "clay":
          requirements[robot_type] = (value[0],int(qty), value[2],value[3])
        elif src_type == "obsidian":
          requirements[robot_type] = (value[0],value[1],int(qty),value[3])
        else:
          requirements[robot_type] = (value[0],value[1],value[2], int(qty))

  return bp_number, tuple(requirements)

robot_types = {
  "ore":0,
  "clay":1,
  "obsidian":2,
  "geode":3,
}

ORE=0
CLAY=1
OBSIDIAN=2
GEODE=3

@lru_cache(maxsize=None)
def solve(bp_number:int,
          MAX_ORE_REQUIRED, time: int,
          stock: Tuple[int,int,int,int],
          robots: Tuple[int,int,int,int],
          all_requirements: Tuple[Tuple[int,int,int,int]]):
  time += 1
  if time > 24:
    return stock[GEODE]

  # Produce new stock
  new_stock = (stock[0] + robots[0],
               stock[1] + robots[1],
               stock[2] + robots[2],
               stock[3] + robots[3])
  
  best = new_stock[GEODE]
  if time < 24:
    if stock[ORE] < MAX_ORE_REQUIRED:
      # Choose not to make a robot because we are saving up
      best = max(new_stock[GEODE], solve(bp_number, MAX_ORE_REQUIRED, time, new_stock, robots, all_requirements))

    for type in range(4):
      requirements = all_requirements[type]
      worth_it = True
      if type == CLAY and time > 19: worth_it=False
      if type == OBSIDIAN and time > 21: worth_it=False
      if worth_it and \
            stock[0] >= requirements[0] and \
            stock[1] >= requirements[1] and \
            stock[2] >= requirements[2] and \
            stock[3] >= requirements[3]:
        reduced_stock = (new_stock[0] - requirements[0],
                        new_stock[1] - requirements[1],
                        new_stock[2] - requirements[2],
                        new_stock[3] - requirements[3])
        if type == 0:
          new_robots = (robots[0] + 1,robots[1],robots[2],robots[3])
        elif type == 1:
          new_robots = (robots[0],robots[1] + 1,robots[2],robots[3])
        elif type == 2:
          new_robots = (robots[0],robots[1],robots[2]+1,robots[3])
        else:
          new_robots = (robots[0],robots[1],robots[2],robots[3]+1)
        best = max(best,
                  solve(bp_number, MAX_ORE_REQUIRED, time,reduced_stock, new_robots, all_requirements))

  return best


with open(f"C:\Personal\AdventOfCode2022\Day19\data.txt") as f:
  lines = f.read().splitlines()

  quality=0
  for line in lines:
    bp_number, requirements = parse_line(line)
    
    initial_stock = (0,0,0,0)
    built_robots = (1,0,0,0)
    MAX_ORE_REQUIRED = max(q[0] for q in requirements)
    best = solve(bp_number, MAX_ORE_REQUIRED, 0, initial_stock, built_robots, requirements)
    print(best)
    quality += (bp_number * best)
  print(quality)   #1714

