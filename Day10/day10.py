from typing import Dict


with open("Day10/data.txt") as f:
  clock = 0
  register_x = 1
  register_x_history: Dict[int, int] = dict()  #clock cycle to value
  for command in f:
    match command.strip().split():
      case ["noop"]:
        register_x_history[clock+1] = register_x
        clock+=1
      case ["addx", value]:
        register_x_history[clock+1] = register_x
        register_x_history[clock+2] = register_x
        register_x += int(value)
        clock+=2
      case _:
        pass
    
  part1 = sum(clk * register_x_history[clk] for clk in [20,60,100,140,180,220])
  print(part1)

  for row in range(0, 6):
    for column in range(0, 40):
      middle_sprint_position = register_x_history[1 + column + (row * 40)]
      if abs(middle_sprint_position-column) <= 1:
        print("#", end="")
      else:
        print(".", end="")
    print("")