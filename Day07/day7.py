
from typing import Dict, List
DIR_SEP = "\\"

with open("Day07/data.txt") as f:
  lines: List[str] = f.read().splitlines()
  path: List[str] = []
  directories: Dict[str, int] = dict()
  current_path = ""

  for line in lines:
    if line.startswith("$ cd .."):
      path = path[:-1]
      current_path = DIR_SEP.join(path)
      print(line, current_path)
    elif line.startswith("$ cd "):
      sub_folder = line.removeprefix("$ cd ")
      path.append(sub_folder)
      current_path = DIR_SEP.join(path)
      print(line, current_path)

      if current_path not in directories:
        directories[current_path] = 0
    elif line.startswith("$ ls"):
      # list
      pass
    elif line.startswith("dir "):
      # subfolder
      pass
    else:
      # file
      text_size, filename = line.split(" ")
      size = int(text_size)
      directories[current_path] += size

def directory_size(directory: str, directories: Dict[str,int]) -> int:
  s = sum([directories[sub] 
           for sub in directories
           if sub.startswith(directory + DIR_SEP)
          ])
  return directories[directory] + s
         

for d in directories:
  print(f"{d} {directories[d]} ({directory_size(d, directories)})")

part1 = sum(t for d in directories 
            if (t:= directory_size(d, directories)) <= 100000)
print(part1)
assert part1 == 1844187