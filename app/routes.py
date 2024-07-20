from flask import render_template, Blueprint, jsonify

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
    threading.Thread(target=simulate_verdicts, args=(plano,)).start()
    return render_template('plano_result.html', plano=plano)

# Rota para a coleta do status
@bp.route('/api/vereditos/<plano>')
def get_verdicts(plano):
    selected_verdicts = verdicts.get(plano, ['pending', 'pending', 'pending', 'pending'])
    return jsonify(selected_verdicts)

@bp.route('/api/status/<plano>')
def get_status(plano):
    selected_verdicts = verdicts.get(plano, ['pending', 'pending', 'pending', 'pending'])
    if 'pending' in selected_verdicts:
        return jsonify({"status": "pending"})
    else:
        return jsonify({"status": "complete"})
