from collections import defaultdict
from typing import DefaultDict


with open("Day01/data.txt") as f:
  lines = f.readlines()

elf_number = 0
totals: DefaultDict[int, int] = defaultdict(int)

for line_number, line in enumerate(lines):
  if line == "\n":
    elf_number += 1
  else:
    totals[elf_number] += int(line.strip("\n"))

print(max(totals.values()))
