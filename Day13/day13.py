from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Data:
  value: Optional[int]
  sub_data: List["Data"]

  def convert_to_list(self) -> "Data":
    assert self.value is not None
    return Data(None, [Data(self.value,[])])

  def __str__(self) -> str:
    if self.value:
      return str(self.value)
    else:
      return "[" + ",".join([str(d) for d in self.sub_data]) + "]"

def parse_entry(data: str) -> Data:
  data = data.removeprefix("[").removesuffix("]")

  if data == "":
    return Data(None, [])

  if data.isnumeric():
    return Data(int(data), [])

  i = 0
  open_count = 0
  element_start = 0
  parts: List[Data] = []
  while i < len(data):
    if data[i] == "[":
      open_count+=1
    elif data[i] == "]":
      open_count-=1
    elif data[i] == "," and open_count == 0:
      element = data[element_start:i]
      parts.append(parse_entry(element))
      element_start = i+1
    i+=1
    
  element = data[element_start:i]
  parts.append(parse_entry(element))
  return Data(None, parts)

def compare(left: Data, right:Data) -> Optional[bool]:
  # print(f"{left} vs {right}")
  if left.value is not None and right.value is not None:
    if left.value < right.value:
      return True
    elif left.value > right.value:
      return False
    else:
      return None
    
  if left.value is not None and right.value is None:
    left = left.convert_to_list()

  if left.value is None and right.value is not None:
    right = right.convert_to_list()

  for i in range(len(left.sub_data)):
    if i >= len(right.sub_data):
      # RHS has ran out of items
      return False

    cmp = compare(left.sub_data[i],right.sub_data[i])
    if cmp == True:
      return True
    elif cmp == False:
      return False
    else:
      # Keep checking
      pass
  
  # Did the lhs run out?
  if len(right.sub_data) > len(left.sub_data):
    return True

  return None

with open("Day13/data.txt") as f:
  pairs = [p.split("\n") for p in f.read().split("\n\n")]
  correct = 0
  for indices, pair in enumerate(pairs):
    lhs = parse_entry(pair[0])
    rhs = parse_entry(pair[1])
    if compare(lhs, rhs):
      correct+=(indices+1)
  print(correct)

 
# lhs = parse_entry("[]")
# rhs = parse_entry("[3]")
# assert compare(lhs, rhs)

