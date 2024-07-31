from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db():
    from .models import SensorData, Sensor, Sistema, Plano, Vereditos

    db.create_all()

    # Verifica e adiciona status do sistema
    if not Sistema.query.first():
        db.session.add(Sistema(status="livre"))
        db.session.commit()
