# Python Hints and Tricks

## Day 1
* `\n\n` will split lines which are seperated by blank lines into groups.
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

To avoid the overheading of storing values in memory,  a generator can be used.  This has the disadvantage of being slower.

``` Python
def splits(lines: List[str]):
  for line in lines:
    yield line[1:3]
```

To perform integer division the `//` operator can be used.  For _integers_ this is the same as math.floor(a/b).


## Day 4
To check if two ranges `(a0,b0)` and `(a1,b1)` overlap the following can be used.
`a0 <= b1 and b0 >= a0`

If you are ensure why this works,  I find it helpful to draw out each of the possible cases on paper.

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
For problems involving custom comparsions the dunder methods such as __lt__ can be defined on a class.  The other comparsion methods (gt) can be automatically defined by adding the `@total_ordering` decorator.  To use the `@total_ordering` decorator `eq` __should__ also be defined. 

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

To find the bounds of the grid
```Python
min_x = min([x for (x,_) in grid])
max_x = max([x for (x,_) in grid])
min_y = min([y for (_,y) in grid])
max_y = max([y for (_,y) in grid])
```

 






