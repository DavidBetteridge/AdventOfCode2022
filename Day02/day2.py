WIN = 6; DRAW = 3; LOSE = 0
ROCK = 1; PAPER = 2; SCISSORS = 3

part1_scores = {
  "A X": DRAW + ROCK,
  "A Y": WIN + PAPER,
  "A Z": LOSE + SCISSORS,
  "B X": LOSE + ROCK,
  "B Y": DRAW + PAPER,
  "B Z": WIN + SCISSORS,
  "C X": WIN + ROCK,
  "C Y": LOSE + PAPER,
  "C Z": DRAW + SCISSORS,
}

part2_scores = {
  "A X": LOSE + SCISSORS,
  "A Y": DRAW + ROCK,
  "A Z": WIN + PAPER,
  "B X": LOSE + ROCK,
  "B Y": DRAW + PAPER,
  "B Z": WIN + SCISSORS,
  "C X": LOSE + PAPER,
  "C Y": DRAW + SCISSORS,
  "C Z": WIN + ROCK,
}

with open("Day02/data.txt") as f:
  rounds = f.read().splitlines()

print("Part1", sum(part1_scores[round] for round in rounds))
print("Part2", sum(part2_scores[round] for round in rounds))
