from typing import List, Optional


class Node:
  def __init__(self, data: int):
    self.data = data
    self.next: "Node" = self
    self.prev: "Node" = self
  def __str__(self) -> str:
    return str(self.data)
  def __repr__(self) -> str:
    return str(self.data)

def print_list(tail):
  n = tail
  for _ in range(len(original_order)):
    print(n.data)
    n=n.next
  print("")

with open(f"C:\Personal\AdventOfCode2022\Day20\data.txt") as f:
  tail = None
  head = None
  zero = None
  original_order: List[Node] = []
  for line in f:
    value = int(line.strip())
    node = Node(value)
    original_order.append(node)

    if node.data == 0:
      zero = node

    if tail is None:
      tail = node

    if head is None:
      head = node
    else:
      head.next = node
      node.prev = head
      head = node
    head.next = tail
    tail.prev = head

for mix_idx in range(len(original_order)):
  mix = original_order[mix_idx]
  for _ in range(abs(mix.data)):
    prev = mix.prev
    prev_prev = mix.prev.prev
    next = mix.next
    next_next = mix.next.next
    if mix.data > 0:
      prev.next = next
      next.prev = prev
      next.next = mix
      mix.prev = next
      mix.next = next_next
      next_next.prev = mix
    else:
      prev_prev.next = mix
      mix.prev = prev_prev
      mix.next = prev
      prev.prev = mix
      prev.next = next
      next.prev = prev

answer = 0
n = zero
for _ in range(1000):
  n = n.next
answer += n.data  
for _ in range(1000):
  n = n.next
answer += n.data  
for _ in range(1000):
  n = n.next
answer += n.data  

print(answer)