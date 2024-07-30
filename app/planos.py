from .lib.jpmsb import sensor
from .database import db
from .models import Sensor, StatusPlano

from loguru import logger


def plano_temperatura(ow_sensor):
    # Verifica cada sensor registrado
    sensors_addresses = ow_sensor.list_sensors()
    for index, sensor_address in enumerate(sensors_addresses):
        try:
            temperature = ow_sensor.get_temperature(index + 1)
            logger.debug(sensor_address)
            logger.debug(temperature)
        except Exception as e:
            logger.warning(f"Erro ao obter temperatura do sensor {sensor_address}")
            logger.debug(e)
            continue
            
        # Veredito
        if not temperature:
            continue

        if temperature > 30:
            verdict = "fail"
        else:
            verdict = "pass"
        
        # Verifica se o sensor já foi registrado
        sensor_data = Sensor.query.filter_by(serialNumber=sensor_address).first()
        if sensor_data:
            sensor_data.temperature = temperature
            sensor_data.verdict = verdict
            db.session.add(sensor_data)
            continue
        else:
            sensor_data = Sensor(
                serialNumber=sensor_address, temperature=temperature, verdict=verdict
            )
            db.session.add(sensor_data)
        
    # Encontra status do plano e altera para complete
    status = StatusPlano.query.filter_by(plano="temperatura").first()
    status.status = "complete"
    db.session.add(status)

    # Salva no banco de dados
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error("Erro ao salvar no banco de dados")
        logger.debug(e)


def plano_curto(ow_sensor):
    logger.info("Inicio plano de curto")
    # Encontra status do plano e altera para complete
    status = StatusPlano.query.filter_by(plano="curto").first()
    status.status = "complete"
    db.session.add(status)

    # Salva no banco de dados
    db.session.commit()


def plano_pinos(ow_sensor):
    logger.info("Inicio plano de pinos")
    # Encontra status do plano e altera para complete
    status = StatusPlano.query.filter_by(plano="pinos").first()
    status.status = "complete"
    db.session.add(status)

    # Salva no banco de dados
    db.session.commit()


# Plano de testes de temperatura
def seleciona_plano(app_context, plano):
    app_context.push()
    ow_sensor = sensor("app/temp/sys/bus/w1/devices")

    if plano == "temperatura":
        plano_temperatura(ow_sensor=ow_sensor)
    elif plano == "curto":
        plano_curto(ow_sensor=ow_sensor)
    elif plano == "pinos":
        plano_pinos(ow_sensor=ow_sensor)
    else:
        logger.warning("Plano não existe")
