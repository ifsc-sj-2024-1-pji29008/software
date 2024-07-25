from .lib.jpmsb import sensor
from .database import db
from .models import Sensor, StatusPlano

from loguru import logger

# Plano de testes de temperatura
def test_temp(app_context):
    app_context.push()
    ow_sensor = sensor("app/temp/sys/bus/w1/devices")

    # Verifica cada sensor registrado
    sensors_addresses = ow_sensor.list_sensors()
    for index, sensor_address in enumerate(sensors_addresses):
        logger.debug(sensor_address)
        logger.debug(ow_sensor.get_temperature(index + 1))

        temperature = ow_sensor.get_temperature(index + 1)
        address = sensor_address

        # Veredito
        if temperature > 40:
            verdict = "fail"
        else:
            verdict = "pass"

        # Salvar o resultado no banco de dados
        sensor_data = Sensor(
            serialNumber=address, temperature=temperature, verdict=verdict
        )
        db.session.add(sensor_data)

        # Encontra status do plano e altera para complete
        status = StatusPlano.query.filter_by(plano="temperatura").first()
        status.status = "complete"
        db.session.add(status)

        # Salva no banco de dados
        db.session.commit()
