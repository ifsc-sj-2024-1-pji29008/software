from lib.jpmsb import onewire

import os


# Plano de testes de temperatura
def test_temp():
    
    sensor = onewire('../temp/sys/bus/w1/devices')   
    