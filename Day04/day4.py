with open("Day04/data.txt") as f:
  lines = f.read().splitlines()
  part1_count = 0
  part2_count = 0
  for line in lines:
    elf1, elf2 = line.split(",")
    elf1_start, elf1_end = [int(r) for r in elf1.split("-")]
    elf2_start, elf2_end = [int(r) for r in elf2.split("-")]

    if (elf1_start <= elf2_start and elf1_end >= elf2_end) or \
       (elf2_start <= elf1_start and elf2_end >= elf1_end):
      part1_count+=1

    if elf1_start <= elf2_end and elf1_end >= elf2_start:
      part2_count+=1

assert part1_count == 536
assert part2_count == 845

print(part1_count, part2_count)
