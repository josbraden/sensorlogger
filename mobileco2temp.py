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
import csv
import os
from datetime import datetime

# Variables
pollinterval = 30
failSleep = 120
# If True, assume we're never home, even if we are
logHome = False
workingDir = "/home/pi"
dataDir = workingDir + "/data"
# DB Stuff
dbhost = "127.0.0.1"
dbuser = "dbuser"
dbpasswd = "password"
dbschema = "sensors"
dbcompress = False
# These should be fine unless you also altered the schema file
dbcharset = "utf8mb4"
dbcollation = "utf8mb4_general_ci"


# Function to test database connection
def testMySQL():
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
        connectioncursor.execute("SELECT COUNT(*) FROM mobileco2")
        connresult = connectioncursor.fetchone()
        for i in connresult:
            print("Success")

        connectioncursor.close()
        connection.close()
        return 0


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

    query = "INSERT INTO mobiletemperature (temp,time) VALUES ('"
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


# Function to upload data files to the database server
def uploadData():
    for filename in os.listdir(dataDir):
        fullFileName = dataDir + "/" + filename
        fp = open(fullFileName, 'r')
        reader = csv.reader(fp)
        for row in reader:
            ret = insertData(str(row[1]), str(row[2]), str(row[0]))
            if ret:
                print("Error inserting data")
                fp.close()
                return ret

        fp.close()
        os.remove(fullFileName)


# Function to read data from sensor and write to a CSV
def readsensor(mon, filename):
    data = mon.read_data()
    fp = open(filename, 'a')
    writer = csv.writer(fp)
    writer.writerow(data)
    fp.close()
    return 0


# Function to check if we're at home or now
# If we're at home, don't log data, instead upload data file(s)
def checkHome():
    if logHome:
        return False

    elif dbhost != "127.0.0.1" and testMySQL:
        return True

    else:
        return False


# Main function
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

if checkHome():
    uploadData()
    # TODO add an auto shutdown mode that runs updates and powers off

else:
    mon = co2meter.CO2monitor(bypass_decrypt=True)
    filename = dataDir + "mobileco2-" + (str(datetime.now())).replace(" ", ".") + ".csv"
    while True:
        ret = readsensor(mon, filename)
        time.sleep(pollinterval)
