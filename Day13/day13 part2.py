from dataclasses import dataclass
from typing import List, Optional
from functools import cmp_to_key 

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

def sort_compare(left: Data, right:Data) -> int:
  match compare(left, right):
    case True:
      return -1
    case False:
      return 1
    case _:
      return 0

with open("Day13/data.txt") as f:
  lines = [parse_entry(p) for p in f.read().splitlines() if p != ""]
  d1 = parse_entry("[[2]]")
  d2 = parse_entry("[[6]]")
  lines.append(d1)
  lines.append(d2)

  lines.sort(key=cmp_to_key(sort_compare))
  i1 = lines.index(d1)+1
  i2 = lines.index(d2)+1
  print(i1*i2)


