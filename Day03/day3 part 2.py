from string import ascii_letters
from typing import Callable, Iterator, List, Set, Tuple

SplitsType = Iterator[Tuple[Set[str],...]]

def part1_splits(rucksacs: List[str]) -> SplitsType:
  for line in rucksacs:
    first = set(line[:len(line)//2])
    second = set(line[len(line)//2:])
    yield (first, second)

def part2_splits(rucksacs: List[str]) -> SplitsType:
  r = 0
  while r < len(rucksacs):
    a = set(rucksacs[r])
    b = set(rucksacs[r+1])
    c = set(rucksacs[r+2])
    r += 3
    yield (a,b,c)

def solve(rucksacks: List[str], split_fn: Callable[[List[str]], SplitsType]):
  score = 0
  for group in split_fn(rucksacks):
    duplicates = group[0]
    for other_group in group[1:]:
      duplicates = duplicates.intersection(other_group)
    score += sum([ascii_letters.index(letter)+1 for letter in duplicates])
  return score

with open("Day03/data.txt") as f:
  rucksacs = f.read().splitlines()
  part1_score = solve(rucksacs, part1_splits)
  part2_score = solve(rucksacs, part2_splits)

assert part1_score == 8185
assert part2_score == 2817

print(part1_score, part2_score)
