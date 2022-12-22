import networkx as nx

reverse_directions = {
  "R": "L",
  "D" : "U",
  "L" : "R",
  "U" : "D"
}

with open("Day22/data.txt") as f:
  rows = f.read().splitlines()
  n_rows = len(rows) -2
  n_columns = max([len(row) for row in rows[:-2]])
  commands = rows[-1]
  current_location = None
  current_direction = "R"
  G = nx.DiGraph()
  for row_number, row in enumerate(rows[:-2]):
    row_start = min(x for x, cell in enumerate(row) if cell != " ")

    for column_number, cell in enumerate(row):
      column_start = min(y for y, row in enumerate(rows[:-2]) if column_number < len(row) and row[column_number] != " ")
      column_end = max(y for y, row in enumerate(rows[:-2]) if column_number < len(row) and row[column_number] != " ")

      if cell == ".":
        G.add_node((column_number, row_number))
        if current_location is None:
          current_location = (column_number, row_number)

        dirs = [(-1,0,"L"),(1,0,"R"),(0,-1,"U"),(0,1,"D")]
        for x_off,y_off,direction in dirs:
          x = column_number + x_off
          if direction == "R" and x >= len(row): x = row_start
          if direction == "L" and x < row_start: x = len(row)-1

          y = row_number + y_off
          if direction == "D" and y >= (column_end+1): y = column_start
          if direction == "U" and y < column_start: y = column_end

          if x < len(rows[y]) and rows[y][x] == ".":
            G.add_edge((column_number, row_number),(x,y),direction=direction)
            G.add_edge((x,y), (column_number, row_number),direction=reverse_directions[direction])

  moves = {
    "R": (1,0),
    "L": (-1,0),
    "U": (0,-1),
    "D": (0,1),
  }

  left_turns = {
    "R": "U",
    "D" : "R",
    "L" : "D",
    "U" : "L"
  }

  right_turns = {
    "R": "D",
    "D" : "L",
    "L" : "U",
    "U" : "R"
  }

  turns = {
    "R" : right_turns,
    "L" : left_turns
  }

  scores = {
    "R": 0,
    "D" : 1,
    "L" : 2,
    "U" : 3
  }

  #10R5L5R10L4R5L5
  i = 0
  while i < len(commands):
    command = ""
    while i < len(commands) and commands[i].isdigit():
      command += commands[i]
      i += 1
    if command != "":
      # We have a distance
      x_off,y_off = moves[current_direction]
      for _ in range(int(command)):
        valid_moves = [edge for edge in G.out_edges(current_location,data=True)
                       if edge[2]["direction"]==current_direction]
        if len(valid_moves)>0:
          current_location = valid_moves[0][1]
        else:
          break
      
    else:
      # We have a direction
      current_direction = turns[commands[i]][current_direction]
      i+=1
    # print(current_location, current_direction)

  print(current_location, current_direction)

  print(  (1000 * (current_location[1]+1)) + (4 * (current_location[0]+1)) + scores[current_direction])

  #118380 toolow