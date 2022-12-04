with open("Day04/data.txt") as f:
  lines = f.read().splitlines()
  count = 0
  for line in lines:
    elf1, elf2 = line.split(",")
    elf1_start, elf1_end = [int(r) for r in elf1.split("-")]
    elf2_start, elf2_end = [int(r) for r in elf2.split("-")]

    if elf1_start <= elf2_start and elf1_end >= elf2_end:
      count+=1
    elif elf2_start <= elf1_start and elf2_end >= elf1_end:
      count+=1

print(count)  # 536
