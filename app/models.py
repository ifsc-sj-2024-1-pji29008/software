from datetime import datetime
from enum import Enum

from .database import db
from loguru import logger


def salva_no_banco(dados):
    db.session.add(dados)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error("Erro ao salvar no banco de dados")
        logger.debug(e)

class PlanoNome(Enum):
    TEMP = "temperatura"
    CURTO = "curto"
    PINOS = "pinos"

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_position = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    sensor = db.relationship("Sensor", backref=db.backref("sensor_data", lazy=True))
    plano = db.relationship("Plano", backref=db.backref("sensor_data", lazy=True))

    def add_sensorData(self):
        salva_no_banco(self)
        
    def get_sensorData(plano_id, sensor_id):
        sensor_data = SensorData.query.filter_by(plano_id=plano_id, sensor_id=sensor_id).all()
        return sensor_data

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serialNumber = db.Column(db.String(50), nullable=False, unique=True)

    def add_sensor(self):
        salva_no_banco(self)

    def find_sensor(serialNumber):
        sensor = Sensor.query.filter_by(serialNumber=serialNumber).first()   
        return sensor
    
class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="esperando")
    timestamp = db.Column(db.DateTime, default=datetime.now, unique=True)

    def add_status(novoStatus):
        salva_no_banco(novoStatus)
    
    def alter_status(novoStatus):
        plano = Plano.query.first()
        plano.status = novoStatus
        return plano
    
    def get_id(id):
        id = Plano.query.get(id)
        return id

class Vereditos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=False)
    resultado = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    comentario = db.Column(db.Text)
    sensor = db.relationship("Sensor", backref=db.backref("vereditos", lazy=True))
    sensor_position = db.Column(db.Integer, nullable=False)
    plano = db.relationship("Plano", backref=db.backref("vereditos", lazy=True))

    def add_veredito(self):
        salva_no_banco(self)

class Sistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default="livre")

    def add_status(novoStatus):
        salva_no_banco(novoStatus)

    def find_sistema():
        sistema = Sistema.query.first()
        return sistema
    
    def alter_status(novoStatus):
        sistema = Sistema.query.first()
        sistema.status = novoStatus
        return sistema
    