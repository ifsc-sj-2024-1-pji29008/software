from .jiga_data import planos_info

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from .models import SensorData, Sensor, StatusPlano
    db.create_all()
    
    # Verifica e adiciona planos do planos_info
    for plano_key, plano_info in planos_info.items():
        if not StatusPlano.query.filter_by(plano=plano_key).first():
            new_plano = StatusPlano(plano=plano_key, status='pending')
            db.session.add(new_plano)
    db.session.commit()
