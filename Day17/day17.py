grid = {}
width = 7

rocks = [
  {"width": 4, "offsets": [(0,0),(1,0),(2,0),(3,0)]},       # Horizonal - Line
  {"width": 3, "offsets": [(1,0),(0,1),(1,1),(2,1),(1,2)]}, # Cross
  {"width": 3, "offsets": [(0,0),(1,0),(2,0),(2,1),(2,2)]}, # L
  {"width": 1, "offsets": [(0,0),(0,1),(0,2),(0,3)]},       # Vertical - Line
  {"width": 2, "offsets": [(0,0),(0,1),(1,0),(1,1)]}        # Square
]

def highest_rock_or_floor():
  if len(grid) > 0:
    return max(y for _,y in grid)
  else:
    return -1

def is_valid(left_edge, bottom_edge, rock) -> bool:
  for x,y in rock["offsets"]:
    if left_edge+x < 0 or left_edge+x > 6: return False
    if bottom_edge+y < 0: return False
    if grid.get((left_edge+x,bottom_edge+y)," ")=="#": return False
  return True

def print_grid(grid):
  for row in range(highest_rock_or_floor()+5, -1, -1):
    for column in range(7):
      cell = grid.get((column,row)," ")
      print(cell,end="")
    print("")
  print("=======")

def apply(grid, left_edge, bottom_edge, rock):
  t = grid.copy()
  for x,y in rock["offsets"]:
    t[(left_edge+x,bottom_edge+y)]="@"
  return t

with open(r"Day17/data.txt") as f:
  jets = f.read()

jet_index = 0
rock_index = 0

for _ in range(2022):
  rock = rocks[rock_index]
  rock_index = (rock_index + 1)
  if rock_index == len(rocks):
    rock_index = 0

  highest_rock = highest_rock_or_floor()
  bottom_edge = highest_rock + 4
  left_edge = 2
  right_edge = left_edge + rock["width"] - 1

  left_right = True
  while True:
    if left_right:
      if jets[jet_index] == ">":
        if is_valid(left_edge+1, bottom_edge,rock):
          left_edge += 1
          right_edge += 1
      else:
        if is_valid(left_edge-1, bottom_edge,rock):
          left_edge -= 1
          right_edge -= 1

      jet_index = (jet_index + 1)
      if jet_index == len(jets):
        jet_index = 0
    else:
      if is_valid(left_edge, bottom_edge-1,rock):
        bottom_edge -=1
      else:
        break
    left_right = not left_right

  for x,y in rock["offsets"]:
    grid[(left_edge+x,bottom_edge+y)]="#"

assert highest_rock_or_floor()+1 == 3147
