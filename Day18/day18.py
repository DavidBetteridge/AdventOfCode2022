from typing import Dict, Tuple
import time

st = time.time()
with open(r"C:\Personal\AdventOfCode2022\Day18\data.txt") as f:
  lines = f.read().splitlines()

  cubes = set()
  for cube in lines:
    x,y,z = cube.split(",")
    cubes.add((int(x),int(y),int(z)))

  
  edges = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
  possible_exposed_edges = []
  for cube in cubes:
    x,y,z=cube
    for (ox,oy,oz) in edges:
      if (x+ox,y+oy,z+oz) not in cubes:
        possible_exposed_edges.append((x+ox,y+oy,z+oz))

  assert len(possible_exposed_edges) == 4308 #4308


  minX = min(x for x,y,z in cubes)
  minY = min(y for x,y,z in cubes)
  minZ = min(z for x,y,z in cubes)
  maxX = max(x for x,y,z in cubes)
  maxY = max(y for x,y,z in cubes)
  maxZ = max(z for x,y,z in cubes)

  examined: Dict[Tuple[int,int,int],bool] = dict()
  def is_outside(cube):
    if cube in examined: return examined[cube]
    queue = [cube]
    seen = set()
    while len(queue) > 0:
      next_cube = queue.pop()
      seen.add(next_cube)
      x,y,z = next_cube

      if x < minX or x > maxX or y< minY or y > maxY or z< minZ or z > maxZ:
        # Must be outside
        for c in seen:
          examined[c]=True
        return True

      for (ox,oy,oz) in edges:
        if (x+ox,y+oy,z+oz) not in cubes and (x+ox,y+oy,z+oz) not in seen:
          queue.append((x+ox,y+oy,z+oz))

    for c in seen:
      examined[c]=False
    return False

  total = 0
  for possible_exposed_edge in possible_exposed_edges:
    if is_outside(possible_exposed_edge):
      total +=1
  print(total)
  assert total == 2540

  
  elapsed_time = time.time() - st
  print(total, 'Total time:', elapsed_time, 'seconds')