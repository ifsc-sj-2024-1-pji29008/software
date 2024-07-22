from flask import Flask

from audioop import add
from .lib.jpmsb import onewire
from .database import db
from .models import Sensor, StatusPlano

import enum
from time import sleep
from loguru import logger

# Plano de testes de temperatura
def test_temp():
    ow = onewire('sys/bus/w1/devices')
    sensors = {}
    # Garantir que o sensor foi encontrado
    barramentos = ow.list_w1_buses()
    # Coletar dados do sensor
    for i, bar in enumerate(barramentos):
        logger.debug(bar)
        sensors = ow.list_sensors(i+1)
        for j, sensor in enumerate(sensors):            
            logger.debug(ow.get_address(i+1, j+1))
            logger.debug(ow.get_temperature(i+1, j+1))
            temperature = ow.get_temperature(i+1, j+1)
            address = ow.get_address(i+1, j+1)
            # Veredito
            if temperature > 40:
                verdict = "fail"
            else:
                verdict = "pass"
            
            # Salvar o resultado no banco de dados
            sensor_data = Sensor(serialNumber=address, temperature=temperature, verdict=verdict)
            db.session.add(sensor_data)
            
            # Encontra status do plano 3 e altera para complete
            status = StatusPlano.query.filter_by(plano='plano3').first()
            status.status = 'complete'
            db.session.add(status)          
            
            # Salva no banco de dados
            db.session.commit()
    
    
