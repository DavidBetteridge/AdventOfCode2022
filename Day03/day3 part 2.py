
def score_duplicate(duplicate:str):
  if duplicate.islower():
    return ord(duplicate) - ord('a') + 1
  else:
    return ord(duplicate) - ord('A') + 27

with open("Day03/data.txt") as f:
  rucksacs = f.read().splitlines()
  score = 0
  r = 0
  while r < len(rucksacs):
    a = set(rucksacs[r])
    b = set(rucksacs[r+1])
    c = set(rucksacs[r+2])
    r += 3
    duplicates = a.intersection(b).intersection(c)
    score += sum([score_duplicate(dup) for dup in duplicates])

print(score)
