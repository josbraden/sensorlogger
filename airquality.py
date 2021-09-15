# Logs air quality data
# Tested using DEVMO PM Sensor SDS011
# @author Josh Braden

import serial
import time
import mysql.connector

# Variables
pollinterval = 5
failSleep = 30
upperLevel = 1000
# DB Stuff
dbhost = "127.0.0.1"
dbuser = "dbuser"
dbpasswd = "password"
dbschema = "sensors"
dbcompress = False
# These should be fine unless you also altered the schema file
dbcharset = "utf8mb4"
dbcollation = "utf8mb4_general_ci"


# Function to insert sensor data to database
def insertData(pmtwofive, pmten):
    query = "INSERT INTO airquality (pmtwofive, pmten) VALUES ("
    query += str(pmtwofive) + ","
    query += str(pmten) + ")"
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)

    except mysql.connector.Error as err:
        print(err)
        return -1

    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        connectioncursor.execute(query)
        connection.commit()
        connectioncursor.close()
        connection.close()

    return 0


# Function to read data from sensor
def readsensor():
    ser = serial.Serial('/dev/ttyUSB0')
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10
    # Ignore anomalously large values
    if pmtwofive > upperLevel or pmten > upperLevel:
        ret = 1

    else:
        ret = insertData(pmtwofive, pmten)

    return ret


# Main function
while True:
    ret = readsensor()
    if ret == 0:
        time.sleep(pollinterval)

    elif ret == 1:
        print("Ignored a large sensor value")
        time.sleep(pollinterval)

    else:
        print("Error logging data")
        time.sleep(failSleep)
