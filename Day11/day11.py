from dataclasses import dataclass
from typing import List

@dataclass
class Monkey:
  number: int
  items: List[int]
  operation: str
  test_divisor: int
  true_monkey: int
  false_monkey: int
  activity: int

with open("Day11/data.txt") as f:
  lines = f.read().splitlines()

  monkeys:List[Monkey] = []
  line_number = 0
  while line_number < len(lines):
    number = int(lines[line_number].removeprefix("Monkey ").removesuffix(":"))
    line_number+=1

    items = list(map(int, lines[line_number].strip().removeprefix("Starting items: ").split(", ")))
    line_number+=1

    operation = lines[line_number].strip().removeprefix("Operation: ")
    line_number+=1

    test_divisor = int(lines[line_number].strip().removeprefix("Test: divisible by "))
    line_number+=1

    true_monkey = int(lines[line_number].strip().removeprefix("If true: throw to monkey "))
    line_number+=1

    false_monkey = int(lines[line_number].strip().removeprefix("If false: throw to monkey "))
    line_number+=1
    line_number+=1

    monkeys.append(Monkey(number,items,operation,test_divisor,true_monkey,false_monkey, 0))

  for _ in range(20):
    for monkey in monkeys:
      while monkey.items:
        monkey.activity += 1
        old = monkey.items.pop(0)
        new = 0
        exec(monkey.operation)
        new = new // 3
        if new % monkey.test_divisor == 0:
          monkeys[monkey.true_monkey].items.append(new)
        else:
          monkeys[monkey.false_monkey].items.append(new)


  activities = sorted([monkey.activity for monkey in monkeys], reverse=True)
  part1 = activities[0]*activities[1]
  print(part1)