from collections import defaultdict


grid = {}
width = 7

rocks = [
  {"width": 4, "offsets": [(0,0),(1,0),(2,0),(3,0)]},       # Horizonal - Line
  {"width": 3, "offsets": [(1,0),(0,1),(1,1),(2,1),(1,2)]}, # Cross
  {"width": 3, "offsets": [(0,0),(1,0),(2,0),(2,1),(2,2)]}, # L
  {"width": 1, "offsets": [(0,0),(0,1),(0,2),(0,3)]},       # Vertical - Line
  {"width": 2, "offsets": [(0,0),(0,1),(1,0),(1,1)]}        # Square
]

def is_valid(left_edge, bottom_edge, rock) -> bool:
  for x,y in rock["offsets"]:
    if left_edge+x < 0 or left_edge+x > 6: return False
    if bottom_edge+y < 0: return False
    if grid.get((left_edge+x,bottom_edge+y)," ")=="#": return False
  return True

def print_grid(grid):
  for row in range(max(heights)+5, max(heights)+5-30, -1):
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

with open(r"C:\Personal\AdventOfCode2022\Day17\data.txt") as f:
  jets = f.read()
jet_index = 0
rock_index = 0
heights = [-1] * 7
heights_by_rocks = {}

for i in range(10000):
  rock = rocks[rock_index]
  rock_index = (rock_index + 1)
  if rock_index == len(rocks):
    rock_index = 0

  highest_rock = max(heights)
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
    heights[left_edge+x] = max(bottom_edge+y, heights[left_edge+x])

  heights_by_rocks[i] =  max(heights)


# print_grid(grid)
print(max(heights)+1)
# assert  max(heights)+1 == 3147 #3147

s=""
for i in range(len(heights_by_rocks)-1):
  s+=str(heights_by_rocks[i+1]-heights_by_rocks[i])


# prefix = 0
# for i in range(434):
#   prefix += heights_by_rocks[i]

# repeat_height = 0
# for i in range(434, 1710):
#   repeat_height += heights_by_rocks[i]

# print(heights_by_rocks[434], heights_by_rocks[434+1710] - heights_by_rocks[434])

# height at 434 == 713
# height at 434+1710 (2143) = 713 + 2620 + 1 = 3334
# height at 434+1710+1710 (3854) = 713 + 2620 + 2620 + 1= 5953
# height at 434+1710+1710+1710 (5564) = 713 + 2620 + 2620 + 2620 + 1= 8574

print(heights_by_rocks[434+926] - heights_by_rocks[434])

# 1000000
# 656
# 713 + (2620*584795321)+1025   #1532163742758
# 713 + (2620*584795321)+1025   #1532163742758

# 713 + (2620*584)+1+ 1439

# 926 short

# (1000000-434)-(584*1710)

# (1000000-434)//1710
# 1532232
# 1532233