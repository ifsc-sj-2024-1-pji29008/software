from re import S
from venv import logger
from .planos import test_temp
from .database import db
from .models import Sensor, StatusPlano

from flask import render_template, Blueprint, jsonify
from loguru import logger

import time
import  threading

bp = Blueprint('main', __name__)

# Devem ser substituídos por chamadas ao banco de dados
verdicts = {
    'plano1': ['pending', 'pending', 'pending', 'pending'],
    'plano2': ['pending', 'pending', 'pending', 'pending'],
    'plano3': ['pending', 'pending', 'pending', 'pending']
}

# Função para simular a execução dos testes
def simulate_verdicts(plano):
    time.sleep(10)  # Simula o tempo de execução dos testes (10 segundos)
    verdicts[plano] = ['pass', 'pass', 'fail', 'pass']  # Define os vereditos de exemplo

# Rota para a página inicial
@bp.route('/')
def index():
    return render_template('index.html')

# Rota para a página de resultados
@bp.route('/plano/<plano>')
def plano_result(plano):    
    # Simulando a execução dos testes em uma thread
    # threading.Thread(target=simulate_verdicts, args=(plano,)).start()
    # threading.Thread(target=test_temp,).start()
    test_temp()
    
    return render_template('plano_result.html', plano=plano)

# Rota com os vereditos dos testes
@bp.route('/api/vereditos')
def get_verdicts():
    # Coleta os vereditos do banco de dados
    veredicts = Sensor.query.all()
    to_send = []
    for i in range(0, 4):
        logger.info(veredicts[i].verdict)
        to_send.append(veredicts[i].verdict)

    
    
    return jsonify(to_send)

# Simula a coleta do status
@bp.route('/api/status/<plano>')
def get_status(plano):
    # Coleta o status do plano
    logger.debug(plano)
    status = StatusPlano.query.filter_by(plano=plano).first()
    status = status.status
    print(status)
    if status == 'pending':
        return jsonify({"status": "pending"})
    elif status == 'complete':
        return jsonify({"status": "complete"})