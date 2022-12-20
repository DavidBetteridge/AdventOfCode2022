from typing import  List, Tuple
from functools import lru_cache


def parse_line(line: str) -> Tuple[int,Tuple[Tuple[int,int,int],...]]:
  bp, robots = line.split(":")
  bp_number = int(bp[9:])

  requirements: List[Tuple[int,int,int]] = []
  for _ in range(4):
    requirements.append((0,0,0))

  for robot in robots.strip().split("."):
    if robot != "":
      lhs, costs = robot.strip()[4:].split(" robot costs ")
      robot_type = robot_types[lhs.strip()]
      for cost in costs.split(" and "):
        qty, src_type = cost.split(" ")
        value = requirements[robot_type]
        if src_type == "ore":
          requirements[robot_type] = (int(qty),value[1],value[2])
        elif src_type == "clay":
          requirements[robot_type] = (value[0],int(qty), value[2])
        else:
          requirements[robot_type] = (value[0],value[1],int(qty))

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

def solve_blueprint(all_requirements: Tuple[Tuple[int,int,int],...],
                    time_allowed: int):
  initial_stock = (0,0,0,0)
  built_robots = (1,0,0,0)
  MAX_ORE_REQUIRED = max(q[ORE] for q in all_requirements[:-1])
  MAX_CLAY_REQUIRED = max(q[CLAY] for q in all_requirements[:-1])  
  
  @lru_cache(maxsize=None)
  def solve(time: int,
            stock: Tuple[int,int,int,int],
            robots: Tuple[int,int,int,int]):
    time += 1
    if time > time_allowed:
      return stock[GEODE]

    # Produce new stock
    new_stock = (stock[0] + robots[0],
                stock[1] + robots[1],
                stock[2] + robots[2],
                stock[3] + robots[3])
    
    best = new_stock[GEODE]
    if time < time_allowed:
      # Always build Geode if we can
      requirements = all_requirements[GEODE]
      if stock[ORE] >= requirements[ORE] and \
        stock[OBSIDIAN] >= requirements[OBSIDIAN]:
        new_robots = (robots[0],robots[1],robots[2],robots[3]+1)
        reduced_stock = (new_stock[ORE] - requirements[ORE],
                          new_stock[1],
                          new_stock[OBSIDIAN] - requirements[OBSIDIAN],
                          new_stock[3])
        best = max(best,
                  solve(time,reduced_stock, new_robots))
      else:
        done_something = False
        can_create_ore = stock[ORE] >= all_requirements[ORE][ORE]
        can_create_clay = stock[ORE] >= all_requirements[CLAY][ORE] 
        can_create_obsidian = (stock[ORE] >= all_requirements[OBSIDIAN][ORE]) and \
                              (stock[CLAY] >= all_requirements[OBSIDIAN][CLAY])
        if (not can_create_ore) or (not can_create_clay) or (not can_create_obsidian):
          # Save up
          best = max(best, solve(time, new_stock, robots))
          done_something = True

        for type in range(3):
          requirements = all_requirements[type]
          worth_it = True
          if type == CLAY and (time > (time_allowed-5)): worth_it=False
          if type == ORE and (time > (time_allowed-3)): worth_it=False
          if type == OBSIDIAN and (time > (time_allowed-3)): worth_it=False
          if worth_it \
                and ((type == ORE and can_create_ore) \
                or (type == CLAY and can_create_clay) \
                or (type == OBSIDIAN and can_create_obsidian)):
            reduced_stock = (new_stock[0] - requirements[0],
                            new_stock[1] - requirements[1],
                            new_stock[2] - requirements[2],
                            new_stock[3])
            if type == 0:
              new_robots = (robots[0] + 1,robots[1],robots[2],robots[3])
            elif type == 1:
              new_robots = (robots[0],robots[1] + 1,robots[2],robots[3])
            else:
              new_robots = (robots[0],robots[1],robots[2]+1,robots[3])
            best = max(best,
                      solve(time,reduced_stock, new_robots))
            done_something = True
        if not done_something:
          best = max(best, solve(time, new_stock, robots))

    return best
  return solve(0, initial_stock, built_robots)


with open(r"C:\Personal\AdventOfCode2022\Day19\data.txt") as f:
  lines = f.read().splitlines()

  quality=0
  for line in lines:
    bp_number, requirements = parse_line(line)
    best = solve_blueprint(requirements, time_allowed=24)
    print(bp_number, best)
    quality += (bp_number * best)
  print(quality)
  assert quality == 62

