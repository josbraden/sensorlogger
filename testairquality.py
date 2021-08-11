# Reads PM sensor once, useful for testing
import serial, time
ser = serial.Serial('/dev/ttyUSB0')
data = []
for index in range(0, 10):
    datum = ser.read()
    data.append(datum)

pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

print("PM 2.5: " + str(pmtwofive))
print("PM 10: " + str(pmten))
