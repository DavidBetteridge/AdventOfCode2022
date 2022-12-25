def snafu_to_number(number):
  total = 0
  for i, c in enumerate(number[::-1]):
    if c == "-":
      total += -1 * (5 ** i) 
    elif c == "=":
      total += -2 * (5 ** i)
    else:
      total += int(c) * (5 ** i)
  return total

with open(r"C:\Personal\AdventOfCode2022\Day25\data.txt") as f:
  numbers = f.read().splitlines()

  sum = 0
  for number in numbers:
    sum += snafu_to_number(number)
  print("Part1", sum)

  # Find the largest power less than the abs value
  p = 0
  while (5 ** p) < abs(sum):
    p+=1
  p=p-1

  answer = ""
  while p >= 0:
    if sum < 0:
      multiples = -round(abs(sum) / (5 ** p))
    else:
      multiples = round(abs(sum) / (5 ** p))
    if multiples == -2:
      answer += "="
    elif multiples == -1:
      answer += "-"
    elif multiples in [2,1,0]:
      answer += str(multiples)
    sum -= multiples * (5 ** p)
    p-=1
  print("Part2", answer)
