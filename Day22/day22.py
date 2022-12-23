from typing import Dict, Tuple
import networkx as nx
from string import ascii_lowercase

reverse_directions = {
  "R": "L",
  "D" : "U",
  "L" : "R",
  "U" : "D"
}

with open("Day22/data.txt") as f:
  rows = f.read().splitlines()
  data_rows =  rows[:-2]
  n_rows = len(data_rows)
  n_columns = max([len(row) for row in data_rows])
  commands = rows[-1]

  # Work out the length of a side on a cube.  To be completely generic
  # we should check the column heights as well,  but we don't need to for
  # our data.
  side_length = len(rows)
  for row in data_rows:
    column_start = min([i for i,c in enumerate(row) if c != " "])
    column_end = len(row)
    side_length = min(side_length, column_end - column_start)

  # Label all the verticies on each face,  from the top-left -> bottom-right
  vertices = {}
  edges = dict()
  for row_number in range(0, n_rows, side_length):
    for column_number in range(0, n_columns, side_length):
      if column_number < len(rows[row_number]) and rows[row_number][column_number] != ' ':
        labels = [ascii_lowercase[len(vertices)+i] for i in range(4)]
        edges[(labels[0],labels[1])]="U"
        edges[(labels[1],labels[3])]="R"
        edges[(labels[0],labels[2])]="L"
        edges[(labels[2],labels[3])]="D"
        for col_off, row_off, label_index in [(0,0,0),(side_length-1,0,1),(0,side_length-1,2),(side_length-1,side_length-1,3)]:
          vertices[labels[label_index]] = ((column_number+col_off, row_number+row_off))

  # Ideally we would find their pairs by folding the net around a centre point
  pairs: Dict[Tuple[str,str],Tuple[str,str]] = {
    ("a","b"): ("u","w"),
    ("e","f"): ("w","x"),
    ("g","h"): ("j","l"),
    ("f","h"): ("t","r"),
    ("s","t"): ("v","x"),
    ("i","k"): ("m","n"),
    ("a","c"): ("o","m"),
    ("u","w"): ("a","b"),
    ("w","x"): ("e","f"),
    ("j","l"): ("g","h"),
    ("r","t"): ("h","f"),
    ("v","x"): ("s","t"),
    ("m","n"): ("i","k"),
    ("m","o"): ("c","a"),
  }

  # pairs: Dict[Tuple[str,str],Tuple[str,str]] = {
  #   ("a","b"): ("f","e"),
  #   ("a","c"): ("i","j"),
  #   ("b","d"): ("x","v"),
  #   ("n","p"): ("v","u"),
  #   ("k","l"): ("q","s"),
  #   ("g","h"): ("t","s"),
  #   ("e","g"): ("x","w"),
  #   ("e","f"):("b","a"),
  #   ("i","j"):("a","c"),
  #   ("v","x"):("d","b"),
  #   ("u","v"):("p","n"),
  #   ("q","s"):("k","l"),
  #   ("s","t"):("h","g"),
  #   ("w","x"):("g","e"),
  # }

  def find_edge(x,y, direction) -> Tuple[str,str]:
    for v1,v2 in edges:
      if edges[(v1,v2)] == direction:
        x1,y1 = vertices[v1]
        x2,y2 = vertices[v2]

        if direction in ("U", "D"):
          if (y == y1) and ((x1 <= x <= x2) or (x2 <= x <= x1)):
            return v1,v2
        else:
          if (x == x1) and ((y1 <= y <= y2) or (y2 <= y <= y1)):
            return v1,v2
    raise Exception("Edge not found")

  def find_offset(edge, x, y):
    v1, v2 = edge
    x1,y1 = vertices[v1]
    x2,y2 = vertices[v2]
    if x1 == x2:
      assert y1 < y2
      distance = y - y1
    else:
      assert x1 < x2
      distance = x - x1
    assert 0 <= distance < 50
    return distance

  def apply_offset(opposite_edge, offset) -> Tuple[int, int]:
    v1, v2 = opposite_edge
    x1,y1 = vertices[v1]
    x2,y2 = vertices[v2]

    if x1 == x2:
      x = x1
      if y1 < y2:
        y = y1 + offset
      else:
        y = y1 - offset
    else:
      if x1 < x2:
        x = x1 + offset
      else:
        x = x1 - offset
      y = y1

    assert min(x1,x2) <= x <= max(x1,x2)
    assert min(y1,y2) <= y <= max(y1,y2)

    return (x,y)

  def switch_side(x,y, direction):
    edge = find_edge(x,y, direction)
    offset = find_offset(edge, x,y)
    opposite_edge = pairs[edge]
    
    a,b = opposite_edge
    if a > b:
      next_direction = edges[(b,a)]
    else:
      next_direction = edges[(a,b)]

    if next_direction == "U":
      next_direction = "D"
    elif next_direction == "D":
      next_direction = "U"
    elif next_direction == "L":
      next_direction = "R"
    elif next_direction == "R":
      next_direction = "L"

    return *apply_offset(opposite_edge, offset),next_direction

  current_location = None
  current_direction = "R"
  G = nx.DiGraph()
  for row_number, row in enumerate(data_rows):
    row_start = min(x for x, cell in enumerate(row) if cell != " ")
    row_end = len(row)-1
    assert row_start % side_length == 0
    assert (row_end+1) % side_length == 0

    for column_number, cell in enumerate(row):
      column_start = min(y for y, row in enumerate(data_rows) if column_number < len(row) and row[column_number] != " ")
      column_end = max(y for y, row in enumerate(data_rows) if column_number < len(row) and row[column_number] != " ")
      assert column_start % side_length == 0
      assert (column_end+1) % side_length == 0

      if cell == ".":
        G.add_node((column_number, row_number))
        if current_location is None:
          current_location = (column_number, row_number)

        dirs = ["L","R","U","D"]
        for direction in dirs:

          if direction == "R":
            if (column_number+1) > row_end:
              next_column_number,next_row_number,next_direction = switch_side(column_number,row_number, direction)
            else:
              next_row_number = row_number
              next_column_number = column_number + 1
              next_direction = direction

          elif direction == "L":
            if (column_number-1) < row_start:
              next_column_number,next_row_number,next_direction = switch_side(column_number,row_number, direction)
            else:
              next_row_number = row_number
              next_column_number = column_number - 1
              next_direction = direction

          elif direction == "U":
            if (row_number-1) < column_start:
              next_column_number,next_row_number,next_direction = switch_side(column_number,row_number, direction)
            else:
              next_column_number = column_number
              next_row_number = row_number - 1
              next_direction = direction

          elif direction == "D":
            if (row_number+1) > column_end:
              next_column_number,next_row_number,next_direction = switch_side(column_number,row_number, direction)
            else:
              next_column_number = column_number
              next_row_number = row_number + 1
              next_direction = direction

          else:
            raise Exception("Unknown direction")

          if rows[next_row_number][next_column_number] == ".":
            G.add_edge((column_number, row_number),(next_column_number,next_row_number),direction=direction,next_direction=next_direction)
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

  i = 0
  debug = {}
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
          current_direction = valid_moves[0][2]["next_direction"]
          debug[current_location] = current_direction
        else:
          break
      
    else:
      # We have a direction
      current_direction = turns[commands[i]][current_direction]
      debug[current_location] = current_direction
      i+=1
    # print(current_location, current_direction)

  print(current_location, current_direction)

  print(  (1000 * (current_location[1]+1)) + (4 * (current_location[0]+1)) + scores[current_direction])

  #101048 toolow
  # not 147040
  #10R5L5R10L4R5L5

  for row_number in range(0, n_rows):
    for column_number in range(0, n_columns):
      cd = debug.get((column_number,row_number),"")
      if cd == "":
        if column_number < len(rows[row_number]):
          print(rows[row_number][column_number],end="")
        else:
          print(" ",end="")
      else:
        print(cd,end="")
    print("")
