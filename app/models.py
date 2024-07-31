from datetime import datetime
from enum import Enum

from .database import db


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


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serialNumber = db.Column(db.String(50), nullable=False, unique=True)


class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="esperando")
    timestamp = db.Column(db.DateTime, default=datetime.now, unique=True)


class Vereditos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey("plano.id"), nullable=False)
    resultado = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    comentario = db.Column(db.Text)
    sensor = db.relationship("Sensor", backref=db.backref("vereditos", lazy=True))
    plano = db.relationship("Plano", backref=db.backref("vereditos", lazy=True))


class Sistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default="livre")
