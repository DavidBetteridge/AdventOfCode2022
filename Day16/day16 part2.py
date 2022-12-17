from collections import defaultdict
import re
import time
import networkx as nx
from itertools import product

open_valves = {}
flow_rates = {}

def remove_node(G, node: str):
  in_edges = list(G.in_edges(node,data=True))
  out_edges = list(G.out_edges(node,data=True))

  for in_edge,_,d_in in in_edges:
    for _,out_edge,d_out in out_edges:
      if in_edge != out_edge and not G.has_edge(in_edge, out_edge):
        G.add_edge(in_edge, out_edge, distance=d_in["distance"]+d_out["distance"])
  G.remove_node(node)

with open(r"C:\Personal\AdventOfCode2022\Day16\data.txt") as f:
  # Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
  lines = f.read().splitlines()
  pattern = r"Valve (?P<valve>[A-Z]+) has flow rate=(?P<rate>[\d]+); tunnel[s]? lead[s]? to valve[s]? "

  G = nx.DiGraph()

  for line in lines:
    m = re.match(pattern, line)
    if not m:
      raise Exception("Parse error")
    valve = m.group("valve")
    rate = int(m.group("rate"))
    if "valves" in line:
      leads_to = line.split("valves ")[1].split(", ")
    else:
      leads_to = line.split("valve ")[1].split(", ")

    open_valves[valve]=False
    flow_rates[valve]=rate

    G.add_node(valve, rate=rate)
    for target in leads_to:
      G.add_edge(valve, target, distance=1)

  to_remove = [node[0] for node in G.nodes(data=True)
                if node[1]["rate"] == 0 and node[0] != 'AA']
  for node in to_remove:
    remove_node(G, node)

  path_lengths = defaultdict(dict)
  for src in G.nodes():
    for dst in G.nodes():
      if src != dst:
        distance = nx.shortest_path_length(G, src, dst, weight="distance")
        path_lengths[src][dst] = distance

  def solve(G, your_location, elephant_location, moves_renamining, total_flow,
            your_distance_to_walk: int, elephant_distance_to_walk: int) -> int:
    
    if your_distance_to_walk > 2 and elephant_distance_to_walk > 2:
      smallest = min(your_distance_to_walk, elephant_distance_to_walk)-1
      your_distance_to_walk -= smallest
      elephant_distance_to_walk -= smallest
      moves_renamining -= smallest

    moves_renamining -= 1
    if moves_renamining <= 0:
      return total_flow




    # Do you need to take a step?
    your_possible_moves=[]
    you_opened_valve=False
    if your_distance_to_walk > 0:
      your_possible_moves = [(your_location, your_distance_to_walk -1)]
    else:
      if not open_valves[your_location]:
        total_flow += moves_renamining * flow_rates[your_location]
        open_valves[your_location]=True
        you_opened_valve=True

    # Does the elephant need to take a step?
    elephant_possible_moves=[]
    elephant_opened_valve=False
    if elephant_distance_to_walk > 0:
      elephant_possible_moves = [(elephant_location, elephant_distance_to_walk -1)]
    else:
      if not open_valves[elephant_location]:
        total_flow += moves_renamining * flow_rates[elephant_location]
        open_valves[elephant_location]=True
        elephant_opened_valve=True

      # Where can you go next?
    if len(your_possible_moves) == 0:
      for next_location,distance in path_lengths[your_location].items():
        if open_valves[next_location]==False and distance < moves_renamining:
          your_possible_moves.append((next_location, distance))

    # Where can the elephant go next?
    if len(elephant_possible_moves) == 0:
      for next_location,distance in path_lengths[elephant_location].items():
        if open_valves[next_location]==False and distance < moves_renamining:
          elephant_possible_moves.append((next_location, distance))

    best_total_flow = total_flow

    if len(your_possible_moves) > 0 or len(elephant_possible_moves) > 0:
      if len(your_possible_moves) == 0:
        your_possible_moves = [(your_location, 9999)]
      if len(elephant_possible_moves) == 0:
        elephant_possible_moves = [(elephant_location, 9999)]

      best = max([solve(G, next_location, next_ele_location, moves_renamining, total_flow, distance1, distance2)
                for (next_location, distance1), (next_ele_location, distance2)
                in product(your_possible_moves,elephant_possible_moves )])
      best_total_flow = max(best_total_flow, best)

    if you_opened_valve: open_valves[your_location]=False
    if elephant_opened_valve: open_valves[elephant_location]=False

    return best_total_flow

  st = time.time()
  total = solve(G, "AA", "AA", 27, 0, 0, 0)
  elapsed_time = time.time() - st
  print(total, 'Total time:', elapsed_time, 'seconds')
  assert total == 1707


