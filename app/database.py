from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from .models import SensorData
    db.create_all()
