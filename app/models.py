# Define your database models here
from sqlalchemy import Column, ForeignKey, Integer, String
from datetime import datetime
from . import db

class Sensor(db.Model):
    __tablename__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    serialNumber = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    verdict = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)
    data = db.relationship('SensorData',backref='sensor')
    
    def __repr__(self):
        return f'Sensor {self.id}'
    
    # Consultando todas as informações de um sensor
    @classmethod
    def find_sensor(cls, session, id):
        sensor = session.query(cls).filter_by(id=id).all()
        for aux in sensor:
            print(sensor.id, sensor.serialNumber, sensor.verdict, sensor.type, sensor.description)
        return sensor

    # Adicionando um novo sensor
    @classmethod
    def add_sensor(cls, serialNumber, type, verdict, description=None):
        new_sensor = cls(serialNumber=serialNumber, type=type, verdict=verdict, description=description)
        db.session.add(new_sensor)
        db.session.commit()

    # Consultando todas informações de todos os sensores
    @classmethod
    def list_all_sensors(cls, session):
        sensors = session.query(cls).all()
        for sensor in sensors:
            print(sensor.id, sensor.verdict, sensor.type, sensor.description)
        return sensors

class SensorData(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, ForeignKey('sensor.id'), nullable=False)
    dateTime = db.Column(db.DateTime, default=datetime.now, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    # sensor = db.relationship('Sensor',backref='data', lazy=True)  # Adicionando o backref para a relação inversa)

    def __repr__(self):
        return f'Data {self.id}'
    
    # Consultando a temperatura de um sensor
    @classmethod
    def find_temperature(cls, session, id):
        temperature = session.query(cls).filter_by(id=id).all()
        for data in temperature:
            print(data.temperature)
        return temperature

    # Alterando novos valores de dados de um sensor
    def add_data(cls, id, dateTime, temperature):
        new_valors = cls(id=id, dateTime=dateTime, temperature=temperature) 
        db.session.add(new_valors)
        db.session.commit()

class StatusPlano(db.Model):
    __tablename__ = 'planos'

    id = db.Column(db.Integer, primary_key=True)
    plano = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')

    def __repr__(self):
        return f'Planos {self.id}'
    
    @classmethod
    def list_all_planos(cls, session):
        planos = session.query(cls).all()
        for plano in planos:
            print(plano.id, plano.plano, plano.status)
        return planos
