import re
from dataclasses import dataclass
from typing import List, Set, Tuple


@dataclass
class Location:
  x: int
  y: int

@dataclass
class Sensor:
  sensor: Location
  beacon: Location

def distance(lhs: Location, rhs: Location)->int:
  return abs(lhs.x-rhs.x) + abs(lhs.y-rhs.y)

pattern = r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
with open(r"C:\Personal\AdventOfCode2022\Day15\data.txt") as f:
  lines = f.read().splitlines()
  sensors:List[Sensor] = []
  for line in lines:
    m = re.match(pattern, line)
    if not m:
      raise Exception("Parse error")
    sensor = Sensor(
      Location(int(m.group("sensor_x")), int(m.group("sensor_y"))),
      Location(int(m.group("beacon_x")), int(m.group("beacon_y"))))
    sensors.append(sensor)

  min_x = 0
  min_y = 0
  max_x = 4000000
  max_y = 4000000
  # tuning_frequency = (x * 4000000) + y
  # sample_target_frequence = 56000011

  
  no_beacon_xs: List[List[Tuple[int,int]]] = []
  for _ in range(max_y+1):
    no_beacon_xs.append([])

  for sensor in sensors:
    m_dist = distance(sensor.sensor, sensor.beacon)
    for target_row in range(max(0, sensor.sensor.y - m_dist), min(max_x, sensor.sensor.y + m_dist+1)):
      distance_to_row = abs(sensor.sensor.y - target_row)
      remaining = m_dist - distance_to_row
      if remaining >=0:
        no_beacon_xs[target_row].append((max(0,sensor.sensor.x - remaining),
                                      min(max_x, sensor.sensor.x + remaining)))

  def overlaps(a:Tuple[int,int],b:Tuple[int,int]) -> bool:
    return a[0] <= (b[1]+1) and b[0] <= (a[1]+1)

  def combine(a:Tuple[int,int],b:Tuple[int,int]) -> Tuple[int,int]:
    return min(a[0],b[0]),max(a[1],b[1])

  for y in range(max_y+1):
    ranges = no_beacon_xs[y]
    try_again = True

    final_ranges: List[Tuple[int,int]] = []
    while len(ranges) > 0:
      r = ranges.pop()
      for i, o in enumerate(ranges):
        if overlaps(r,o):
          ranges.pop(i)
          ranges.append(combine(o,r))
          break
      else:
        final_ranges.append(r)

    final_ranges = sorted(final_ranges)
    if final_ranges[0][0] != 0 or final_ranges[0][1] != max_x:
      tuning_frequency = ((final_ranges[0][1]+1)  * 4000000) + y
      print(y, tuning_frequency)
      break



