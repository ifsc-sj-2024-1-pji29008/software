from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from .models import SensorData, Sensor, StatusPlano
    db.create_all()
    
    # Verifica se já existem dados no banco de dados
    if StatusPlano.query.count() > 0:
        pass
    else:
        # Adiciona status para 3 planos
        status1 = StatusPlano(plano='plano1', status='pending')
        status2 = StatusPlano(plano='plano2', status='pending')
        status3 = StatusPlano(plano='plano3', status='pending')
        db.session.add(status1)
        db.session.add(status2)
        db.session.add(status3)
        db.session.commit()
