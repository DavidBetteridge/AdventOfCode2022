from collections import defaultdict


with open("Day01/data.txt") as f:
  lines = [line.strip("\n") for line in f.readlines()]

elf_number = 0
totals = defaultdict(int)

for line_number, line in enumerate(lines):
  if line == "":
    elf_number += 1
  else:
    totals[elf_number] += int(line)

calories = sorted(totals.values(), reverse=True)
print(sum(calories[:3]))