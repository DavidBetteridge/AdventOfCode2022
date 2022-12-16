from collections import defaultdict
import re
import time
import networkx as nx

open_valves = {}
flow_rates = {}

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


  path_lengths = defaultdict(dict)
  for src in G.nodes():
    for dst in G.nodes():
      if src != dst:
        distance = nx.shortest_path_length(G, src, dst)
        path_lengths[src][dst] = distance

  def solve(G, location, moves_renamining, total_flow) -> int:
    if moves_renamining <= 1:
      return total_flow

    if flow_rates[location] > 0:
      moves_renamining -=1
    total_flow += moves_renamining * flow_rates[location]
    best_total_flow = total_flow
    open_valves[location]=True

    for next_location,distance in path_lengths[location].items():
      if flow_rates[next_location] > 0 and open_valves[next_location]==False and distance < moves_renamining:
        best_total_flow = max(best_total_flow, solve(G, next_location, moves_renamining-distance, total_flow))
    open_valves[location]=False


    return best_total_flow

  st = time.time()
  total = solve(G, "AA", 30, 0)
  elapsed_time = time.time() - st
  print(total, 'Total time:', elapsed_time, 'seconds')
  assert total == 2330 #2330 # 1651


