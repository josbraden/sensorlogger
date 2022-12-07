# sensorlogger

Project for logging environment sensor data

## Data Sources

Currently I have two input sources:

- Air quality sensor: DEVMO PM Sensor SDS011
  - This measures PM 2.5 and PM 10
- CO2/Temperature sensor: co2meter.com RAD-0301 Mini

## Setup

- Make a database and user in your MySQL/Mariadb server
- Import DB schema from sensors.sql
- (Optional) test sensors with testairquality.py (don't have a co2 test script yet)
- Run scripts

## Mobile CO2 Stuff

Placeholder, need to write this up. Contains both hardware and software considerations.
