# Python Hints and Tricks

## Day 1
* `\n\n` will split lines which are separated by blank lines into groups.

```Python
totals = [ sum([int(line) 
               for line in block.split("\n")])
               for block in f.read().split("\n\n")]
```

* `heapq.heapify(totals)` will convert the list `totals` into an ordered heap. We can then use `heapq.nlargest(3, totals)` to find the 3 largest values.

## Day 2
A good pattern for reading lines from a text file is
``` Python
with open("Day02/data.txt") as f:
  lines = f.read().splitlines()
```
Unlike doing `f.readlines()` the above approach removes `\n` from the end of each line.

Using a mapping table often provides an easy solution to problems.
```Python
scores = {
  "A X": 0 + 3,
  "A Y": 3 + 1,
  "A Z": 6 + 2,
...
}
```

## Day 3
To find the ASCII/UNICODE value for a character,  use ord.  For example `ord('D')`.  If you want these values to be between 0 and 25,  then subtract the value for 'A' from it.  
ie. `ord('D') - ord('A')`

Set operators can be used for actions such as finding duplicates.
    `duplicates = first.intersection(second)`

To avoid the overhead of storing values in memory,  a generator can be used.  This has the disadvantage of being slower.

``` Python
def splits(lines: List[str]):
  for line in lines:
    yield line[1:3]
```

To perform integer division the `//` operator can be used.  For _integers_ this is the same as math.floor(a/b).


## Day 4
To check if two ranges `(a0,b0)` and `(a1,b1)` overlap the following can be used.
`a0 <= b1 and b0 >= a0`

If you are unsure why this works,  I find it helpful to draw out each of the possible cases on paper.

To check if either range contains the other range.
`(a0 <= a1 and b0 >= b1) or (a1 <= a0 and b1 >= b0)`

## Day 5
Normally we use `list.append(value)` to add an item to end of a list.  However list.`insert(0,value)` can be used to add values to the start of list.

## Day 6
To check if a list contains a duplicate,  we can convert it to a set and then check it's length.
  `contains_duplicates = len(set(window)) < len(window)`

Much quicker approaches of finding if a sliding window contains any duplicates is described here.  https://www.youtube.com/watch?v=U16RnpV48KQ

## Day 7
The newer versions of Python contain pattern matching. This allows us to both match on a pattern and populate place holders.  `sub_folder` in the example below.

```Python
    match line.split():
      case "$", "cd", "..":
        path = path[:-1]
      case "$", "cd", sub_folder:
        path.append(sub_folder)
      case _:
        raise Exception("Should not happen")
```

## Day 8
To iterate over all the entries in a grid,  the following pattern is a good starting point.

```Python
for row_number, row in enumerate(rows):
  for column_number, cell in enumerate(row):
    print(cell)
```

e.g.
```Python
rows = ["ABCD", "EFGH"]
for row_number, row in enumerate(rows):
  print(f"Row={row}", end='')
  for column_number, cell in enumerate(row):
    print(f"  {column_number}={cell}", end='')
  print()
```

Note,  the use of `end=''` suppresses the newline `\n` character.


## Day 9
Python doesn't have a `math.sign` function,  but one can be easily written as follows.

```Python
def sign(a):
    return (a > 0) - (a < 0)
```

and likewise `cmp` (or `compare`) can be written as

```Python
def compare(a, b):
    return (a > b) - (a < b)
```

or more verbosely

```Python
def compare(a: int, b: int) -> int:
  if a > b:
    return 1
  elif b > a:
    return -1
  else:
    return 0
```

## Day 11
The new `removeprefix` and `removesuffix` functions can help with parsing.
`number = int(lines[line_number].removeprefix("Monkey ").removesuffix(":"))`

The `exec` function can use to evaluate expressions, such as `new = old * 19`
e.g.
```Python
old = monkey.items.pop(0)
new = 0   # Defined here to keep the linter happy
exec(monkey.operation)
new = new // 3
```

## Day 12
If you are given a grid,  and need to work with the cells adjacent to each cell.

```Python
for row in range(n_rows):
  for column in range(n_columns):
    for x_offset,y_offset in [(-1,0),(1,0),(0,-1),(0,1)]:
      x = column + x_offset
      y = row + y_offset
      if (0 <= x < n_columns) and (0 <= y < n_rows):
        pass
```

Grids however are graphs in disguise.  If you need to find the shortest path around a grid then the `networkx` library can be used.

```Python
import network as nx
G = nx.DiGraph()
for row in range(n_rows):
  for column in range(n_columns):
    for x_offset,y_offset in [(-1,0),(1,0),(0,-1),(0,1)]:
      x = column + x_offset
      y = row + y_offset
      if (0 <= x < n_columns) and (0 <= y < n_rows):
        G.add_edge((column,row),(x,y))

if nx.has_path(G,source,target):
 print(nx.shortest_path_length(G, source, target))
```


## Day 13
For problems involving custom comparisons the dunder methods such as __lt__ can be defined on a class.  The other comparison methods (gt) can be automatically defined by adding the `@total_ordering` decorator.  To use the `@total_ordering` decorator `eq` __should__ also be defined. 

``` Python
from dataclasses import dataclass
from functools import total_ordering

@total_ordering
@dataclass
class Data:
  value: Optional[int]
  sub_data: List["Data"]

  def __lt__(self, other: "Data"):
      return compare(self, other)
```

## Day 14
Grids can also be held in dictionaries as well as in lists.

`grid: Dict[Tuple[int,int], str] = defaultdict(str)`

To add an item at x=3, y=4 to the grid. `grid[(3,4)] = 'David'`

To find the bounds of the grid we can use
```Python
min_x = min([x for (x,_) in grid])
max_x = max([x for (x,_) in grid])
min_y = min([y for (_,y) in grid])
max_y = max([y for (_,y) in grid])
```

 


## Day 15
Regular expressions can be a good way of parsing the input file.

```Python
pattern = r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
for line in lines:
  m = re.match(pattern, line)
  if m:
    sensor_x = int(m.group("sensor_x"))
```

Remember to cast the result to an int if required.

I normally use https://regex101.com/ in the `Python flavor` to write/test my expressions.


A simple way to time your code is

```Python
import time
st = time.time()
do_stuff()
elapsed_time = time.time() - st
print('Time to do stuff:', elapsed_time, 'seconds')
```


## Day 16

If you have a graph with 6 nodes and 5 edges AA -> . -> . -> BB --> . --> CC
Then this can be reduced to a graph with 3 nodes and 3 edges:
* AA --> BB (Weight/Distance 3)
* BB --> CC (Weight/Distance 2)
* AA --> CC (Weight/Distance 5)

```Python
  path_lengths = defaultdict(dict)
  for src in G.nodes():
    for dst in G.nodes():
      if src != dst:
        distance = nx.shortest_path_length(G, src, dst)
        path_lengths[src][dst] = distance
```

Depth-First-Search can be easily implemented with a recursive algorithm.  For example to sum all the leaf nodes in a tree we walk each branch until we find a node without any children.  We include it's value and then backtrack to the parent node.

```Python
def solve(parent_node):
  if len(parent_node.children) == 0:
    # No children, must be a leaf node
    return parent_node.value
  else:
    # Sum the leaf node values beneath each of our children.
    for child in parent_node.children():
      total += solve(child)
    return total
```

A trick is to reduce the number of branches if a tree we need to consider in order to solve the problem.  For example if we wanted to find the depth of shallowest branch we could keep track of the best result we have found so far,  and then not bother with any branches which are already at least that deep.

```Python
depth = 99999
def solve(parent_node, depth_so_far):
  global depth
  if depth_so_far >= depth:
    # No point check any deeper
    return depth

  if len(parent_node.children) == 0:
    depth = min(depth,depth_so_far)
    return depth_so_far
  else:
    for child in parent_node.children():
      depth_so_far = min(depth_so_far, solve(child, depth_so_far+1))
    return depth_so_far
```



## Day 17
To help with debugging it's often helpful to define a print function early on. For example

```Python
def print_grid(grid):
  for row in range(max(heights)+5, max(heights)+5-30, -1):
    for column in range(7):
      cell = grid.get((column,row)," ")
      print(cell,end="")
    print("")
  print("=======")
```

## Day 18
Although this is a 3D problem,  you can work out your algorithm by drawing it out on paper in 2D


## Day 19
This was a DFS problem which required optimisation.  I used two tricks

1. I added the `@lru_cache(maxsize=None)` decorator to my recursive function so it didn't need to process branches a second time.
2. I used a variation of the `if depth_so_far >= depth:` trick above,  but this time I compared the best score so far with an estimate of the best possible score I could get from this branch.  This estimate must never underestimate it's score as otherwise a potentially winning branch might be skipped.

```Python
@lru_cache(maxsize=None)
def solve(time: int,
          stock: Tuple[int,int,int,int],
          robots: Tuple[int,int,int,int]):
  nonlocal best
  if best > estimate(time,stock,robots):
    return best

```


My recursive `solve` function was nested instead the parent `solve_blueprint` function.  This made the code cleaner,  and also provided a new cache for each blueprint to be processed.
```Python
def solve_blueprint(all_requirements: Tuple[Tuple[int,int,int],...],
                    time_allowed: int):
  best = 0
  @lru_cache(maxsize=None)
  def solve(time: int,
```

## Day 20
If you need to insert/remove items from a middle of a list,  then a double linked list might be a better data structure.

```Python
class Node:
  def __init__(self, data: int):
    self.data = data
    self.next: "Node" = self
    self.prev: "Node" = self
  def __str__(self) -> str:
    return str(self.data)
  def __repr__(self) -> str:
    return str(self.data)

# tail(200) -> middle(150)  -> head(100)
head = Node(100)
middle = Node(150)
tail = Node(200)
tail.next = middle
tail.prev = head
middle.next = head
middle.prev = tail
head.next = tail
head.prev = middle
```

To remove the middle node
```Python
tail.next = head
head.prev = tail
```


## Day 22
You don't need a generic solution to solve the puzzle (unless you want one).  You only need to find the answer for the net you have been given. I labelled all the vertices and then manually worked out which ones would meet on a folded cube.

```Python
pairs: Dict[Tuple[str,str],Tuple[str,str]] = {
     ("a","b"): ("f","e"),
     ("a","c"): ("i","j"),
     ("b","d"): ("x","v"),
     ("n","p"): ("v","u"),
     ("k","l"): ("q","s"),
     ("g","h"): ("t","s"),
     ("e","g"): ("x","w"),
     ("e","f"):("b","a"),
     ("i","j"):("a","c"),
     ("v","x"):("d","b"),
     ("u","v"):("p","n"),
     ("q","s"):("k","l"),
     ("s","t"):("h","g"),
     ("w","x"):("g","e"),
   }
```
You can then do back and replace the mapping with some generic code if you wish.

## Day 24
I made the mistake of taking a short cut on part 1 as I detected that I had an off-by-error from the sample data. For my submission I added one to the answer and that worked.
This came back to haunt me on part 2 which overwise would have been a simple change to my code.

```Python
ENTRANCE = (0, -1)
EXIT = (n_columns-1, n_rows)
leg1 = make_journey(ENTRANCE, EXIT, 0)
leg2 = make_journey(EXIT, ENTRANCE, leg1)
leg3 = make_journey(ENTRANCE, EXIT, leg2)
print("Part1", leg1)
print("Part2", leg3)
```


