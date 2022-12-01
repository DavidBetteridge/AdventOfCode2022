import re
from dataclasses import dataclass
from typing import List, Set


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


  target_row = 2000000
  no_beacon_xs: Set[int] = set()
  for sensor in sensors:
    m_dist = distance(sensor.sensor, sensor.beacon)
    distance_to_row = abs(sensor.sensor.y - target_row)
    remaining = m_dist - distance_to_row
    for x in range(sensor.sensor.x - remaining, sensor.sensor.x + remaining+1):
      if (x != sensor.beacon.x or target_row != sensor.beacon.y): 
        no_beacon_xs.add(x)

  print(len(no_beacon_xs))   # 5073496
