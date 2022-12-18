with open(r"C:\Personal\AdventOfCode2022\Day18\data.txt") as f:
  cubes = f.read().splitlines()

  cache = set()
  for cube in cubes:
    x,y,z = cube.split(",")
    cache.add((int(x),int(y),int(z)))

  
  edges = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]

  total = 0
  for cube in cache:
    x,y,z=cube
    for (ox,oy,oz) in edges:
      if (x+ox,y+oy,z+oz) not in cache:
        total+=1

  assert total == 4308
