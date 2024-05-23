#!/usr/bin/env python3

from jpmsb import onewire

sensor = onewire('sys/bus/w1/devices')

# print(sensor.list_w1_buses())
# print(sensor.list_sensors(2))

print("Sensor na porta 1")
print(sensor.get_address(1,1))
print(sensor.get_temperature(1,1))
print()

print("Sensor na porta 2")
print(sensor.get_address(2,1))
print(sensor.get_temperature(2,1))
print()

print("Sensor na porta 3")
print(sensor.get_address(3,1))
print(sensor.get_temperature(3,1))
print()

print("Sensor na porta 4")
print(sensor.get_address(4,1))
print(sensor.get_temperature(4,1))
print()
