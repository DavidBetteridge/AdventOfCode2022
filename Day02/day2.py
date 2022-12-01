WIN = 6; DRAW = 3; LOSE = 0
ROCK = 1; PAPER = 2; SCISSORS = 3

scores = {
  "A X": (DRAW + ROCK, LOSE + SCISSORS),
  "A Y": (WIN + PAPER, DRAW + ROCK),
  "A Z": (LOSE + SCISSORS, WIN + PAPER),
  "B X": (LOSE + ROCK, LOSE + ROCK),
  "B Y": (DRAW + PAPER, DRAW + PAPER),
  "B Z": (WIN + SCISSORS, WIN + SCISSORS),
  "C X": (WIN + ROCK, LOSE + PAPER),
  "C Y": (LOSE + PAPER, DRAW + SCISSORS),
  "C Z": (DRAW + SCISSORS, WIN + ROCK),
}

with open("Day02/data.txt") as f:
  rows = [scores[round.strip()] for round in f]
  print(*(sum(row[part] for row in rows) for part in (0, 1)))
