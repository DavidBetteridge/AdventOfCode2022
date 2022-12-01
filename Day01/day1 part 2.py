import heapq
with open("Day01/data.txt") as f:
  totals = [ sum([int(line) for line in block.split("\n")]) for block in f.read().split("\n\n")]
heapq.heapify(totals)
print("Part1", sum(heapq.nlargest(1, totals)))
print("Part2", sum(heapq.nlargest(3, totals)))
