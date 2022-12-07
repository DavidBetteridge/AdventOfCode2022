
from collections import defaultdict
from typing import Dict, List
DIR_SEP = "\\"

with open("Day07/data.txt") as f:
  path: List[str] = []
  sizes: Dict[str, int] = defaultdict(int)
  for line in f.read().splitlines():
    match line.split():
      case "$", "cd", "..":
        path = path[:-1]
      case "$", "cd", sub_folder:
        path.append(sub_folder)
      case "$", "ls":
        pass
      case "dir", sub_folder:
        pass
      case text_size, filename:
        for i in range(len(path)):
          sizes[DIR_SEP.join(path[:i+1])] += int(text_size)
      case _:
        raise Exception("Should not happen")

part1 = sum(size for size in sizes.values() if size <= 100000)
print(part1)
assert part1 == 1844187

total_space = 70000000
space_required = 30000000
total_used = sizes["/"]
unused_space = total_space - total_used
min_to_delete = space_required - unused_space
sizes_in_order = sorted([size for size in sizes.values() if size >= min_to_delete ])
part2 = sizes_in_order[0]
print(part2)
assert part2 == 4978279