import json
from dataclasses import dataclass
from typing import  List, Optional
from functools import total_ordering

@total_ordering
@dataclass
class Data:
  value: Optional[int]
  sub_data: List["Data"]

  def convert_to_list(self) -> "Data":
    return Data(None, [Data(self.value,[])])

  def __lt__(self, other: "Data"):
      return compare(self, other)

json_type = int | List["json_type"]
def parse_entry(data: str) -> Data:
  def parse(thing: json_type) -> Data:
    if isinstance(thing, int):
      return Data(thing,[])
    else:
      return Data(None, [parse(c) for c in thing])
  return parse(json.loads(data))

def compare(left: Data, right:Data) -> Optional[bool]:
  if left.value is not None and right.value is not None:
    if left.value < right.value:
      return True
    elif left.value > right.value:
      return False
    else:
      return None
    
  if left.value is not None and right.value is None:
    left = left.convert_to_list()
  elif left.value is None and right.value is not None:
    right = right.convert_to_list()

  for i in range(min(len(left.sub_data), len(right.sub_data))):
    if left.sub_data[i] < right.sub_data[i]:
      return True
    elif left.sub_data[i] > right.sub_data[i]:
      return False
  
  # Did a list run out of entries?
  if len(right.sub_data) > len(left.sub_data):
    return True
  elif len(right.sub_data) < len(left.sub_data):
    return False

  return None

with open("Day13/data.txt") as f:
  lines = [parse_entry(p) for p in f.read().splitlines() if p != ""]
  i1 = len([line for line in lines if line < parse_entry("[[2]]")])+1
  i2 = len([line for line in lines if line < parse_entry("[[6]]")])+2
  part2 = i1*i2
  assert part2 == 21423
