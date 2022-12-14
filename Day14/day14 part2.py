from collections import defaultdict
from typing import Dict, Tuple

def sign(x:int)->int:
  if x < 0:
    return -1
  else:
    return 1

with open("Day14/data.txt") as f:
  lines = f.read().splitlines()

  grid: Dict[Tuple[int,int], str] = defaultdict(str)
  for line in lines:
    parts = line.split(" -> ")

    for i in range(len(parts)-1):
      start = parts[i]
      end = parts[i+1]
      start_x, start_y = start.split(",")
      end_x, end_y = end.split(",")
      x_dir = sign(int(end_x)-int(start_x))
      for x in range(int(start_x), int(end_x)+x_dir, x_dir):
        y_dir = sign(int(end_y)-int(start_y))
        for y in range(int(start_y), int(end_y)+y_dir, y_dir):
          grid[(x,y)] = "#"
  
  min_x = min([x for (x,_) in grid])
  max_x = max([x for (x,_) in grid])
  min_y = min([y for (_,y) in grid])
  max_y = max([y for (_,y) in grid])

  grains_dropped = 0
  sand_location = (500,0)
  while True:
    if sand_location[1]+1 == max_y + 2:
      grid[sand_location]="."
      sand_location = (500,0)
      grains_dropped+=1
      continue

    if grid[(sand_location[0],sand_location[1]+1)] == "":
      sand_location = (sand_location[0],sand_location[1]+1)
    elif grid[(sand_location[0]-1,sand_location[1]+1)] == "":
      sand_location = (sand_location[0]-1,sand_location[1]+1)
    elif grid[(sand_location[0]+1,sand_location[1]+1)] == "":
      sand_location = (sand_location[0]+1,sand_location[1]+1)
    else:
      grains_dropped+=1
      if sand_location == (500,0):
        print(grains_dropped)
        break

      grid[sand_location]="."
      sand_location = (500,0)


# 26484