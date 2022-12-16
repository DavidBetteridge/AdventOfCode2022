import re
import networkx as nx

def remove_node(G, node: str):
  in_edges = list(G.in_edges(node,data=True))
  out_edges = list(G.out_edges(node,data=True))

  for in_edge,_,d_in in in_edges:
    for _,out_edge,d_out in out_edges:
      if in_edge != out_edge and not G.has_edge(in_edge, out_edge):
        G.add_edge(in_edge, out_edge, distance=d_in["distance"]+d_out["distance"])
  G.remove_node(node)

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

  to_remove = [node[0] for node in G.nodes(data=True)
               if node[1]["rate"] == 0 and node[0] != 'AA']
  for node in to_remove:
    remove_node(G, node)


  def solve(G, from_location, location, moves_renamining, total_flow) -> int:
    if moves_renamining <= 1:
      return total_flow

    # Switch on / yes
    # Switch on,  update graph,  increase total_flow,  decrease moves remaining

    # Move from this room without switching on any taps
    best_total_flow = total_flow
    out_edges = list(G.out_edges(location,data=True))
    for _,out_edge,data in out_edges:
      if out_edge != from_location:
        if data["distance"] < moves_renamining:
          best_total_flow = max(best_total_flow, solve(G, location, out_edge, moves_renamining-data["distance"], total_flow))

    is_open = open_valves[location]
    flow = flow_rates[location]
    if flow>0 and not is_open:
      moves_renamining -=1
      total_flow += moves_renamining * flow
      best_total_flow = max(best_total_flow,total_flow)
      open_valves[location]=True
      for _,out_edge,data in out_edges:
        if data["distance"] < moves_renamining:
          best_total_flow = max(best_total_flow, solve(G, location, out_edge, moves_renamining-data["distance"], total_flow))
      open_valves[location]=False


    return best_total_flow


  print(solve(G, "", "AA", 30, 0))  #1651

    



