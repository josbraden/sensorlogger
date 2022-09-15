# This version of the logging script checks if we're online or not, then acts accordingly
# If at home, upload any existing data files to the database server
# If not at home, log co2 and temperature, and the timestamp, to a CSV
# Logs C02 with help from the vfilimonov/co2meter library
# Also logs temperature since that data is recorded with the same instrument
# Device used: CO2Meter RAD-0301 Mini
# Raw device info: {'vendor_id': 1241, 'product_id': 41042,
# 'path': b'1-1.1:1.0', 'manufacturer': 'Holtek',
# 'product_name': 'USB-zyTemp', 'serial_no': '2.00'}
# @author Josh Braden

import time
import co2meter
import mysql.connector

# Variables
pollinterval = 30
failSleep = 120
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
def insertData(co2level, temperature, time):
    query = "INSERT INTO mobileco2 (co2level,time) VALUES ('"
    query += str(co2level) + "," + str(time) + "')"
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

    query = "INSERT INTO temperature (temp_indoor,time) VALUES ('"
    query += str(temperature) + "," + str(time) + "')"
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
def readsensor(mon):
    data = mon.read_data()
    return insertData(data[1], data[2])


# Main function
mon = co2meter.CO2monitor(bypass_decrypt=True)
while True:
    ret = readsensor(mon)
    if ret == 0:
        time.sleep(pollinterval)

    elif ret == 1:
        print("Ignored a large sensor value")
        time.sleep(pollinterval)

    else:
        print("Error logging data")
        time.sleep(failSleep)
