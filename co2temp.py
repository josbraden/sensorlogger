# Logs C02 with help from the vfilimonov/co2meter library
# Also logs temperature since that data is recorded with the same instrument
# Device used: CO2Meter RAD-0301 Mini
# Raw device info: {'vendor_id': 1241, 'product_id': 41042, 'path': b'1-1.1:1.0', 'manufacturer': 'Holtek', 'product_name': 'USB-zyTemp', 'serial_no': '2.00'}
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
def insertData(co2level, temperature):
    query = "INSERT INTO co2 (co2level) VALUES ("
    query += str(co2level) + ")"
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

    query = "INSERT INTO temperature (temp_indoor) VALUES ("
    query += str(temperature) + ")"
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
    mon = co2meter.CO2monitor()
    data = mon.read_data()
    return insertData(data[1], data[2])