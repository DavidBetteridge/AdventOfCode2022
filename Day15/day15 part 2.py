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

  min_x = 0
  min_y = 0
  max_x = 4000000
  max_y = 4000000
  # tuning_frequency = (x * 4000000) + y
  # sample_target_frequence = 56000011

  
  no_beacon_xs: List[Set[int]] = []
  for _ in range(max_y+1):
    no_beacon_xs.append(set())

  for sensor in sensors:
    m_dist = distance(sensor.sensor, sensor.beacon)
    for target_row in range(max_y+1):
      distance_to_row = abs(sensor.sensor.y - target_row)
      remaining = m_dist - distance_to_row
      for x in range(max(0,sensor.sensor.x - remaining), min(max_x+1, sensor.sensor.x + remaining+1)):
        if (x != sensor.beacon.x or target_row != sensor.beacon.y): 
          no_beacon_xs[target_row].add(x)

  for y in range(max_y+1):
    if len(no_beacon_xs[y]) != (max_x+1):
      print(y,  len(no_beacon_xs[y]))