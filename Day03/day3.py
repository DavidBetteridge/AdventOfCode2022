
def score_duplicate(duplicate:str):
  if duplicate.islower():
    return ord(duplicate) - ord('a') + 1
  else:
    return ord(duplicate) - ord('A') + 27

with open("Day03/data.txt") as f:
  score = 0
  for line in f:
    line = line.strip("\n")
    size = int(len(line)/2)
    first = set(line[:size])
    second = set(line[size:])
    duplicates = first.intersection(second)
    score += sum([score_duplicate(dup) for dup in duplicates])

print(score)
