from dataclasses import dataclass
from typing import Dict, Optional, Union

@dataclass
class Node:
  value: Optional[Union[int,str]]
  left: Optional["Node"]
  operation: Optional[str]
  right: Optional["Node"]

  def evaluate(self, nodes: Dict[str, "Node"]):
    if self.value is None:
      lhs = nodes[self.left].evaluate(nodes)
      rhs = nodes[self.right].evaluate(nodes)
      expr = f"({lhs}{self.operation}{rhs})"
      if "?" not in expr and "=" not in expr:
        return int(eval(expr))
      return expr
    return self.value

with open(r"C:\Personal\AdventOfCode2022\Day21\data.txt") as f:
  nodes = {}
  lines = f.read().splitlines()
  for line in lines:
    node_name, expression = line.split(": ")
    node = nodes.get(node_name, None)
    if node is None:
      node = Node(None,None,None,None)
      nodes[node_name] = node
    
    if expression.isdigit():
      node.value = "?" if node_name == "humn" else int(expression)
    else:
      lhs, operator, rhs = expression.split()
      node.left = lhs
      node.operation = operator
      node.right = rhs

  lhs_expr = nodes[nodes["root"].left].evaluate(nodes)
  target = int(nodes[nodes["root"].right].evaluate(nodes))

  def solve(node: Node, target):
    if node.left is None: return target
    lhs_expr = nodes[node.left].evaluate(nodes)
    if str(lhs_expr).isdigit():
      if node.operation == "*":
        target = target / lhs_expr
      elif node.operation == "+":
        target = target - lhs_expr
      elif node.operation == "-":
        target = lhs_expr-target 
      else:
        raise Exception("lhs", node.operation)
      return solve(nodes[node.right], int(target))
      
    rhs_expr = nodes[node.right].evaluate(nodes)
    if str(rhs_expr).isdigit():
      if node.operation == "/":
        target = target * rhs_expr
      elif node.operation == "-":
        target = target + rhs_expr
      elif node.operation == "*":
        target = target / rhs_expr
      elif node.operation == "+":
        target = target - rhs_expr
      else:
        raise Exception("rhs", node.operation)
      return solve(nodes[node.left], int(target))
    raise Exception("None?")

  print(solve(nodes[nodes["root"].left], target))

