from collections import defaultdict


with open("Day05/data.txt") as f:
  lines = f.read().splitlines()

  n = 0
  stacks: defaultdict[int, list[str]] = defaultdict(list)
  num_of_stacks = (len(lines[0])+1) // 4
  while lines[n][1] != "1":
    for s in range(num_of_stacks):
      crate = lines[n][(s*4)+1]
      if crate != " ":
        stacks[s+1].insert(0, lines[n][(s*4)+1])
    n+=1
  n+=2  #Skip the blank line

  for line in lines[n:]:
    lhs, rhs = line.split(" from ")
    qty = int(lhs.split(" ")[1])
    src, dst = rhs.split(" to ")
    for _ in range(qty):
      c = stacks[int(src)].pop()
      stacks[int(dst)].append(c)
    assert line == f"move {qty} from {src} to {dst}"
  for stack in range(num_of_stacks):
    print(stacks[stack+1][-1], end="")   # GTBQZHHVF