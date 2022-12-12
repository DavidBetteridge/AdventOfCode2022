import networkx as nx

def value(symbol:str)->int:
  if symbol == "S":
    return 1
  elif symbol == "E":
    return 26
  else:
    return ord(symbol) - ord("a") + 1

with open("Day12/data.txt") as f:
  grid = f.read().splitlines()

  G = nx.DiGraph()
  sources = []
  target = None
  n_rows = len(grid)
  n_columns = len(grid[0])
  for row in range(n_rows):
    for column in range(n_columns):
      current = value(grid[row][column])
      if current == 1:
        sources.append((column,row))
      elif grid[row][column] == "E":
        target = (column,row)
      for x_offset,y_offset in [(-1,0),(1,0),(0,-1),(0,1)]:
        x = column + x_offset
        y = row + y_offset
        if (0 <= x < n_columns) and (0 <= y < n_rows):
          next = value(grid[y][x])
          if next - current <= 1:
            G.add_edge((column,row),(x,y))

  print(min(nx.shortest_path_length(G, source, target)
        for source in sources
        if nx.has_path(G,source,target)))
