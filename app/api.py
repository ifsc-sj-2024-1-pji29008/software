from .models import Sensor, StatusPlano
from .database import db
from .planos import seleciona_plano

from flask import Blueprint, current_app, jsonify
from loguru import logger

import threading

bp = Blueprint("api", __name__, url_prefix="/api")


# ######
# #   GET
# ######


# @bp.route("/execucoes", methods=["GET"])
# def get_execucoes():
#     # Retorna plano, timestamp, status
#     pass


# @bp.route("/execucoes/<timestamp>", methods=["GET"])
# def get_execucao():
#     # Retorna plano, [sensores(num-serie, veredito, posicao)]
#     pass


# @bp.route("/sensores", methods=["GET"])
# def get_sensores():
#     # Retorna num-serie
#     pass


# @bp.route("/sensores/<numserie>", methods=["GET"])
# def get_sensor():
#     # Retorna num-serie, [(timestamp-execucao, veredito, posicao)]
#     pass


# @bp.route("/sensores/<numserie>/dados", methods=["GET"])
# def get_sensor_dados():
#     # Retorna dados do sensor, com possibilidade de filtrar por timestamp
#     pass


# @bp.route("/status", methods=["GET"])
# def get_stats():
#     # Verifica se existem execucoes em andamento
#     # Se sim, retorna status: "ocupado, timestamp-execucao"
#     # Se não, retorna status: "livre"
#     pass


# ######
# #   POST
# ######


# @bp.route("/reset", methods=["POST"])
# def reset():
#     # Reseta banco de dados
#     pass


# @bp.route("/execucoes", methods=["POST"])
# def inicia_execucao():
#     # Le o corpo da requisicao
#     # Inicia execucao
#     # Retorna timestamp da execucao
#     pass


# Rota com os vereditos dos testes
@bp.route("/execucoes/vereditos")
def get_verdicts():
    # Coleta os vereditos do banco de dados
    verdicts = Sensor.query.all()
    to_send = []
    for i in range(0, 4):
        logger.info(verdicts[i].verdict)
        to_send.append(verdicts[i].verdict)
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
