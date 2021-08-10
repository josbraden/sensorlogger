# Logs air quality data
# Tested using DEVMO PM Sensor SDS011
# @author Josh Braden

import serial
import time

# Variables
pollinterval = 5
# DB Stuff
dbhost = "127.0.0.1"
dbuser = "dbuser"
dbpasswd = "password"
dbschema = "sensors"
dbcompress = False
# These should be fine unless you also altered the schema file
dbcharset = "utf8mb4"
dbcollation = "utf8mb4_general_ci"

# Function to read data from sensor
def readsensor():
    ser = serial.Serial('/dev/ttyUSB0')
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10


# Main function
while True:
    readsensor()
    time.sleep(pollinterval)
