# Define your database models here

from datetime import datetime
from . import db

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    verdict = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    dateTime = db.Column(db.DateTime, default=datetime.now)
    idSerial = db.Column(db.String(50), nullable=False)
    serialNumber = db.Column(db.String(50), nullable=False)    
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    verdict = db.Column(db.String(50), nullable=False)
    serialNumber = db.Column(db.String(50), nullable=False) 
class StatusPlano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plano = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
