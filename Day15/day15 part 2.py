from collections import defaultdict
import re
from dataclasses import dataclass
import time
from typing import Dict, List, Set, Tuple


@dataclass
class Location:
  x: int
  y: int

@dataclass
class Sensor:
  sensor: Location
  beacon: Location
  distance: int = 0

def distance(lhs: Location, rhs: Location)->int:
  return abs(lhs.x-rhs.x) + abs(lhs.y-rhs.y)

st = time.time()

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
    sensor.distance = distance(sensor.sensor, sensor.beacon)
    sensors.append(sensor)

  min_x = 0
  min_y = 0
  max_x = 4000000
  max_y = 4000000
  
  no_beacon_xs: Dict[int, List[Tuple[int,int]]] = defaultdict(list)
  elapsed_time = time.time() - st
  print('PreBuild time:', elapsed_time, 'seconds')

  for sensor in sensors:
    m_dist = sensor.distance
    for target_row in range(max(0, sensor.sensor.y - m_dist), min(max_x, sensor.sensor.y + m_dist+1)):
      remaining = m_dist - abs(sensor.sensor.y - target_row)
      if remaining >=0:
        lower = max(0,sensor.sensor.x - remaining)
        upper = min(max_x, sensor.sensor.x + remaining)
        no_beacon_xs[target_row].append((lower,upper))
  elapsed_time = time.time() - st
  print('Build time:', elapsed_time, 'seconds')

  def overlaps(a:Tuple[int,int],b:Tuple[int,int]) -> bool:
    return a[0] <= (b[1]+1) and b[0] <= (a[1]+1)

  def combine(a:Tuple[int,int],b:Tuple[int,int]) -> Tuple[int,int]:
    return min(a[0],b[0]),max(a[1],b[1])

  for y in range(max_y+1):
    ranges = no_beacon_xs[y]
    n_ranges = len(ranges)
    for i in range(n_ranges-1):
      src = ranges[i]
      for i2 in range(i+1, n_ranges):
        if overlaps(src,ranges[i2]):
          ranges[i2] = combine(src,ranges[i2])
          break
      else:
        elapsed_time = time.time() - st
        print('Found Y:', elapsed_time, 'seconds')        
        ranges = ranges[i:]

        final_ranges: List[Tuple[int,int]] = []
        while len(ranges) > 0:
          r = ranges.pop()
          for i, o in enumerate(ranges):
            if overlaps(r,o):
              ranges[i] = combine(o,r)
              break
          else:
            final_ranges.append(r)

        final_ranges = sorted(final_ranges)
        if final_ranges[0][0] != 0 or final_ranges[0][1] != max_x:
          tuning_frequency = ((final_ranges[0][1]+1)  * 4000000) + y
          print(y, tuning_frequency)
          assert tuning_frequency == 13081194638237
          elapsed_time = time.time() - st
          print('Total time:', elapsed_time, 'seconds')
          break
