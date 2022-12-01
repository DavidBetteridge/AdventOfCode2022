import heapq

with open("Day01/data.txt") as f:
  lines = [line.strip("\n") for line in f.readlines()]

elf_number = 0
totals = [0]

for line_number, line in enumerate(lines):
  if line == "":
    elf_number += 1
    totals.append(0)
  else:
    totals[elf_number] += int(line)

heapq.heapify(totals)
print("Part1", sum(heapq.nlargest(1, totals)))
print("Part2", sum(heapq.nlargest(3, totals)))
