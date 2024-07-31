from .lib.jpmsb import sensor
from .database import db
from .models import Plano, Sensor, PlanoNome, SensorData, Sistema, Vereditos

from loguru import logger


def plano_temperatura(ow_sensor, plano: Plano):
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

        # Encontra sensor no banco de dados
        sen = Sensor.query.filter_by(serialNumber=sensor_address).first()
        if not sen:
            sen = Sensor(serialNumber=sensor_address)
            db.session.add(sen)
            db.session.commit()

        # Verifica se a temperatura foi obtida
        if not temperature:
            continue

        # Verifica se a temperatura é maior que 30
        if temperature > 30:
            verdict = "fail"
        else:
            verdict = "pass"

        db.session.add(
            SensorData(
                plano_id=plano.id,
                sensor_id=sen.id,
                temperature=temperature,
                sensor_position=index + 1,
            )
        )
        db.session.add(
            Vereditos(sensor_id=sen.id, plano_id=plano.id, resultado=verdict)
        )
        # Salva no banco de dados
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Erro ao salvar no banco de dados")
            logger.debug(e)

    # Altera status do plano para complete
    plano.status = "finalizado"
    db.session.add(plano)

    # Encontra status do sistema
    sis = Sistema.query.first()
    sis.status = "livre"
    db.session.add(sis)

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
    sis = Sistema.query.first()
    sis.status = "complete"
    db.session.add(sis)

    # Salva no banco de dados
    db.session.commit()


def plano_pinos(ow_sensor):
    logger.info("Inicio plano de pinos")
    # Encontra status do plano e altera para complete
    sis = Sistema.query.first()
    sis.status = "complete"
    db.session.add(sis)

    # Salva no banco de dados
    db.session.commit()


# Plano de testes de temperatura
def seleciona_plano(app_context, plano_id):
    app_context.push()
    plano = Plano.query.get(plano_id)
    ow_sensor = sensor("app/temp/sys/bus/w1/devices")
    if plano.nome == PlanoNome.TEMP.value:
        plano_temperatura(ow_sensor=ow_sensor, plano=plano)
    elif plano == PlanoNome.CURTO.value:
        plano_curto(ow_sensor=ow_sensor)
    elif plano == PlanoNome.PINOS.value:
        plano_pinos(ow_sensor=ow_sensor)
    else:
        logger.warning("Plano não existe")
