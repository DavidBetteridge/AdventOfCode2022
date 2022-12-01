import time
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

tri = [0,1,3,6,10,15,21,28,36,45,55,61,73]

def solve_blueprint(all_requirements: Tuple[Tuple[int,int,int],...],
                    time_allowed: int):
  initial_stock = (0,0,0,0)
  built_robots = (1,0,0,0)
  best = 0

  def estimate(time: int,
               stock: Tuple[int,int,int,int],
               robots: Tuple[int,int,int,int]):
    used_ore_for_ore = 0
    used_ore_for_clay = 0
    used_ore_for_obs = 0
    used_clay_for_obs = 0
    used_ore_for_geo = 0
    used_obs_for_geo = 0
    for _ in range(time, time_allowed+1):
      if all_requirements[ORE][ORE] <= (stock[ORE] - used_ore_for_ore):
        robots = (robots[ORE]+1,robots[CLAY],robots[OBSIDIAN],robots[GEODE])
        used_ore_for_ore+=all_requirements[ORE][ORE]

      if all_requirements[CLAY][ORE] <= (stock[ORE]- used_ore_for_clay):
        robots = (robots[ORE],robots[CLAY]+1,robots[OBSIDIAN],robots[GEODE])
        used_ore_for_clay+=all_requirements[CLAY][ORE]

      if (all_requirements[OBSIDIAN][ORE] <= (stock[ORE]-used_ore_for_obs)) and \
         (all_requirements[OBSIDIAN][CLAY] <= (stock[CLAY]-used_clay_for_obs)):
        robots = (robots[ORE],robots[CLAY],robots[OBSIDIAN]+1,robots[GEODE])
        used_ore_for_obs+=all_requirements[OBSIDIAN][ORE]
        used_clay_for_obs+=all_requirements[OBSIDIAN][CLAY]

      if (all_requirements[GEODE][ORE] <= (stock[ORE]-used_ore_for_geo)) and \
         (all_requirements[GEODE][OBSIDIAN] <= (stock[OBSIDIAN]-used_obs_for_geo)):
        robots = (robots[ORE],robots[CLAY],robots[OBSIDIAN],robots[GEODE]+1)
        used_ore_for_geo+=all_requirements[GEODE][ORE]
        used_obs_for_geo+=all_requirements[GEODE][OBSIDIAN]

      stock = (stock[0] + robots[0],
                  stock[1] + robots[1],
                  stock[2] + robots[2],
                  stock[3] + robots[3])
    return stock[GEODE]

  @lru_cache(maxsize=None)
  def solve(time: int,
            stock: Tuple[int,int,int,int],
            robots: Tuple[int,int,int,int]):
    nonlocal best
    time += 1
    if time > time_allowed:
      return stock[GEODE]

    if best > estimate(time,stock,robots):
      return best

    # Produce new stock
    new_stock = (stock[0] + robots[0],
                stock[1] + robots[1],
                stock[2] + robots[2],
                stock[3] + robots[3])

    best = max(best, new_stock[GEODE])
    if time < time_allowed:
      # Always build Geode if we can
      requirements = all_requirements[GEODE]
      if stock[ORE] >= requirements[ORE] and \
        stock[OBSIDIAN] >= requirements[OBSIDIAN]:
        if time == (time_allowed-1):
          return 1 + new_stock[GEODE] + robots[GEODE]

        new_robots = (robots[0],robots[1],robots[2],robots[3]+1)
        reduced_stock = (new_stock[ORE] - requirements[ORE],
                          new_stock[1],
                          new_stock[OBSIDIAN] - requirements[OBSIDIAN],
                          new_stock[3])
        best = max(best,
                  solve(time,reduced_stock, new_robots))
      else:
        if time == (time_allowed-1):
          return new_stock[GEODE] + robots[GEODE]

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
  solve(0, initial_stock, built_robots)
  return best

with open(r"C:\Personal\AdventOfCode2022\Day19\data.txt") as f:
  lines = f.read().splitlines()

# Part 1
st = time.time()
quality=0
for line in lines:
  bp_number, requirements = parse_line(line)
  best = solve_blueprint(requirements, time_allowed=24)
  print(bp_number, best)
  quality += (bp_number * best)
print(quality)
assert quality == 1725

elapsed_time = time.time() - st
print('Part 1:', elapsed_time, 'seconds')

# Part 2
st = time.time()
total=1
for line in lines[:3]:
  bp_number, requirements = parse_line(line)
  best = solve_blueprint(requirements, time_allowed=32)
  print(bp_number, best)
  total *= best
print(total)
assert total == 15510

elapsed_time = time.time() - st
print('Part 2:', elapsed_time, 'seconds')