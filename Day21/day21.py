from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class Node:
  value: Optional[int]
  left: Optional["Node"]
  operation: Optional[str]
  right: Optional["Node"]

  def evaluate(self, nodes: Dict[str, "Node"]):
    if self.value is None:
      lhs = nodes[self.left].evaluate(nodes)
      rhs = nodes[self.right].evaluate(nodes)
      if self.operation == "+":
        self.value = lhs + rhs
      if self.operation == "-":
        self.value = lhs - rhs
      if self.operation == "*":
        self.value = lhs * rhs
      if self.operation == "/":
        self.value = lhs / rhs
    return self.value

with open("Day21/data.txt") as f:
  nodes = {}
  lines = f.read().splitlines()
  for line in lines:
    #ptdq: humn - dvpt
    node_name, expression = line.split(": ")
    node = nodes.get(node_name, None)
    if node is None:
      node = Node(None,None,None,None)
      nodes[node_name] = node
    
    if expression.isdigit():
      node.value = int(expression)
    else:
      lhs, operator, rhs = expression.split()
      node.left = lhs
      node.operation = operator
      node.right = rhs

  print(nodes["root"].evaluate(nodes))