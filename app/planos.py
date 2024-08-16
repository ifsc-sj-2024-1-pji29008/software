from .lib.jpmsb import sensor
from .database import db
from .models import Plano, Sensor, PlanoNome, SensorData, Sistema, Vereditos

from loguru import logger

import os

def plano_temperatura(ow_sensor, plano: Plano):
    # Verifica cada sensor registrado
    w1_buses = ow_sensor.list_w1_buses()

    test_repetition = 5
    for index, w1_bus in enumerate(w1_buses):
        sensor_address = None
        temperature = None

        try:
            sensor_address = ow_sensor.get_address(index + 1)
            logger.debug(sensor_address)
        except Exception as e:
            logger.debug(f"Erro ao obter endereco do sensor {index + 1}")
            continue

        # Verifica se um endereco foi obtido
        if not sensor_address:
            continue

        for _ in range(test_repetition):
            try:
                sensor_address = ow_sensor.get_address(index + 1)
                logger.debug(sensor_address)
            except Exception as e:
                logger.debug(f"Erro ao obter endereco do sensor {index + 1}")
                continue

            try:
                temperature = ow_sensor.get_temperature(index + 1)
                logger.debug(temperature)

            except Exception as e:
                logger.warning(f"Erro ao obter temperatura do sensor {sensor_address}")
                logger.debug(e)
                continue



            # Encontra sensor no banco de dados
            sensor = Sensor.find_sensor(sensor_address)
            if not sensor:
                sensor = Sensor(serialNumber=sensor_address)
                sensor.add_sensor()

            # Verifica se a temperatura foi obtida
            if not temperature:
                continue

            # Adiciona os dados no sensor
            sensor_data = SensorData(
                    plano_id=plano.id,
                    sensor_id=sensor.id,
                    temperature=temperature,
                    sensor_position=index + 1,)
            
            sensor_data.add_sensorData()

        # Puxa dados de sensor do banco
        sensor_data = SensorData.get_sensorData(plano.id, sensor.id)

        # Verifica se a temperatura foi obtida
        if not sensor_data:
            continue
        
        # Verifica se a temperatura está dentro do limiar
        verdict = "pass"
        for data in sensor_data:
            if data.temperature < 0 or data.temperature > 30:
                verdict = "fail"
                break

        # Adiciona os veriditos
        vereditos = Vereditos(sensor_id=sensor.id, plano_id=plano.id, resultado=verdict, sensor_position=index + 1)
        
        # Salva no banco de dados
        vereditos.add_veredito()

    # Altera status do plano para complete
    status_plano = Plano.alter_status("finalizado")

    # Encontra status do sistema e altera
    status_sistema = Sistema.alter_status("livre")

    # Salva no banco de dados
    Plano.add_status(status_plano)
    Sistema.add_status(status_sistema)

def plano_curto(ow_sensor):
    logger.info("Início plano de curto")
    # Encontra status do plano e altera para complete
    status_sistema = Sistema.alter_status("complete")

    # Salva no banco de dados
    Sistema.add_status(status_sistema)

def plano_pinos(ow_sensor):
    logger.info("Inicio plano de pinos")
    # Encontra status do plano e altera para complete
    status_sistema = Sistema.alter_status("complete")

    # Salva no banco de dados
    Sistema.add_status(status_sistema)

# Plano de testes de temperatura
def seleciona_plano(app_context, plano_id):
    app_context.push()
    plano = Plano.get_id(plano_id)

    # Check if the environment variable W1_BUS_DIR is set
    if os.environ.get("W1_BUS_DIR"):
        w1_bus_dir = os.environ.get("W1_BUS_DIR")

    # Check if the path /sys/bus/w1/devices exists
    elif os.path.exists("/sys/bus/w1/devices"):
        w1_bus_dir = "/sys/bus/w1/devices"

    # Test path
    else:
        w1_bus_dir = "app/temp/sys/bus/w1/devices"

    logger.debug(f"W1_BUS_DIR: {w1_bus_dir}")
    ow_sensor = sensor(w1_bus_dir)

    if plano.nome == PlanoNome.TEMP.value:
        plano_temperatura(ow_sensor=ow_sensor, plano=plano)
    elif plano == PlanoNome.CURTO.value:
        plano_curto(ow_sensor=ow_sensor)
    elif plano == PlanoNome.PINOS.value:
        plano_pinos(ow_sensor=ow_sensor)
    else:
        logger.warning("Plano não existe")
