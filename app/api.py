import re
from .models import Sensor, StatusPlano
from .database import db
from .planos import seleciona_plano

from flask import Blueprint, jsonify, request, current_app
from loguru import logger
from flasgger import swag_from

import threading

bp = Blueprint("api", __name__, url_prefix="/api")


#################
###    GET   ###
#################

@bp.route("/execucoes", methods=["GET"])
@swag_from('swagger_docs/get_execucoes.yaml')
def get_execucoes():
    fake = {"plano": "plano1", "timestamp": "2021-01-01 00:00:00", "status": "concluido"}
    return jsonify(fake)


@bp.route("/execucoes/<timestamp>", methods=["GET"])
@swag_from('swagger_docs/get_execucao.yaml')
def get_execucao(timestamp):
    fake = {"plano": "plano1", "sensores": [{"num-serie": "123", "veredito": "ok", "posicao": "1"}]}
    return jsonify(fake)


@bp.route("/sensores", methods=["GET"])
@swag_from('swagger_docs/get_sensores.yaml')
def get_sensores():
    fake = {"num-serie": "123"}
    return jsonify(fake)


@bp.route("/sensores/<numserie>", methods=["GET"])
@swag_from('swagger_docs/get_sensor.yaml')
def get_sensor(numserie):
    fake = {"num-serie": "123", "dados": [{"timestamp": "2021-01-01 00:00:00", "veredito": "ok", "posicao": "1"}]}
    return jsonify(fake)


@bp.route("/sensores/<numserie>/dados", methods=["GET"])
@swag_from('swagger_docs/get_sensor_dados.yaml')
def get_sensor_dados(numserie):
    fake = {"num-serie": "123", "dados": [{"timestamp": "2021-01-01 00:00:00", "veredito": "ok", "posicao": "1"}]}
    return jsonify(fake)


@bp.route("/status", methods=["GET"])
@swag_from('swagger_docs/get_status.yaml')
def get_stats():
    fake = {"status": "livre"}
    return jsonify(fake)


#################
###    POST   ###
#################


@bp.route("/reset", methods=["POST"])
@swag_from('swagger_docs/post_reset.yaml')
def reset():
    pass


@bp.route("/execucoes", methods=["POST"])
@swag_from('swagger_docs/post_execucao.yaml')
def inicia_execucao():
    req = request.get_json()
    plano = req.get("plano")
    if not plano:
        return jsonify({"error": "Plano não encontrado"}), 400
    
    status = StatusPlano.query.first()
    if status:
        return jsonify({"error": "Execução em andamento"}), 400
    
    status = StatusPlano(plano=plano)
    db.session.add(status)
    db.session.commit()
    
    thread = threading.Thread(target=seleciona_plano, args=(plano,))
    thread.start()
    
    return jsonify({"message": "Execução iniciada"}), 200



######################
### PARA REMOVER   ###
######################

# Rota com os vereditos dos testes
@bp.route("/vereditos")
def get_verdicts():
    # Coleta os vereditos do banco de dados
    sensor_data = Sensor.query.all()
    to_send = []    
    for sensor in sensor_data:
        to_send.append(
            {
                "serialNumber": sensor.serialNumber,
                "temperature": sensor.temperature,
                "verdict": sensor.verdict,
            }
        )    
    return jsonify(to_send)


# Simula a coleta do status
@bp.route("/status/<plano>", methods=["GET"])
def get_status(plano):
    # Coleta o status do plano
    logger.debug(plano)
    status = StatusPlano.query.filter_by(plano=plano).first()
    status = status.status
    print(status)
    if status == "pending":
        return jsonify({"status": "pending"})
    elif status == "complete":
        return jsonify({"status": "complete"})


# Inicia execução do plano
@bp.route("/iniciar/<plano>", methods=["POST"])
def iniciar_plano(plano):
    # Altera o status do plano para pending
    status = StatusPlano.query.filter_by(plano=plano).first()
    status.status = "pending"
    db.session.add(status)

    try:
        # Salva no banco de dados
        db.session.commit()
        # Inicia o plano
        threading.Thread(
            target=seleciona_plano,
            args=(
                current_app.app_context(),
                plano,
            ),
        ).start()
        return jsonify({"status": "pending"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500