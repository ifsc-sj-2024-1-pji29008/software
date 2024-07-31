import re
from .models import Plano, Sensor, Sistema, PlanoNome
from .database import db, init_db
from .planos import seleciona_plano

from flask import Blueprint, jsonify, current_app
from loguru import logger
from flasgger import swag_from

import threading

bp = Blueprint("api", __name__, url_prefix="/api")


#################
###    GET   ###
#################


@bp.route("/planos", methods=["GET"])
@swag_from("swagger_docs/get_planos.yaml")
def get_planos():
    try:
        planos = Plano.query.all()
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Plano não encontrado"}), 404

    to_send = []
    for plano in planos:
        to_send.append(
            {
                "id": plano.id,
                "nome": plano.nome,
                "timestamp": plano.timestamp,
                "status": plano.status,
            }
        )
    return jsonify(to_send)


@bp.route("/planos/<id>", methods=["GET"])
@swag_from("swagger_docs/get_plano.yaml")
def get_plano(id):
    try:
        plano = Plano.query.filter_by(id=id).first()
    except AttributeError:
        return jsonify({"error": "Plano não encontrado"}), 404

    to_send = {}
    to_send["vereditos"] = []
    for veredito in plano.vereditos:
        to_send["vereditos"].append(
            {
                "id": veredito.id,
                "sensor": veredito.sensor.serialNumber,
                "resultado": veredito.resultado,
                "timestamp": veredito.timestamp,
            }
        )

    to_send["dados"] = []
    for dado in plano.sensor_data:
        to_send["dados"].append(
            {
                "timestamp": dado.timestamp,
                "posicao": dado.sensor_position,
                "temperatura": dado.temperature,
            }
        )
    return jsonify(to_send)


@bp.route("/sensores", methods=["GET"])
@swag_from("swagger_docs/get_sensores.yaml")
def get_sensores():
    try:
        sensores = Sensor.query.all()
    except AttributeError:
        return jsonify({"error": "Sensores não encontrados"}), 404

    to_send = []
    for sensor in sensores:
        to_send.append(sensor.serialNumber)
    return jsonify(to_send)


@bp.route("/sensores/<numserie>", methods=["GET"])
@swag_from("swagger_docs/get_sensor.yaml")
def get_sensor(numserie):

    try:
        sensor = Sensor.query.filter_by(serialNumber=numserie).first()
    except AttributeError:
        return jsonify({"error": "Sensor não encontrado"}), 404

    to_send = {}
    to_send["dados"] = []
    to_send["vereditos"] = []
    for dado in sensor.sensor_data:
        to_send["dados"].append(
            {
                "temperatura": dado.temperature,
                "timestamp": dado.timestamp,
                "posicao": dado.sensor_position,
            }
        )

    for veredito in sensor.vereditos:
        to_send["vereditos"].append(
            {
                "id": veredito.id,
                "planos": veredito.plano.nome,
                "timestamp": veredito.timestamp,
                "resultado": veredito.resultado,
            }
        )
    return jsonify(to_send)


@bp.route("/status", methods=["GET"])
@swag_from("swagger_docs/get_status.yaml")
def get_stats():
    sis = Sistema.query.first()
    return jsonify({"status": sis.status})


#################
###    POST   ###
#################


@bp.route("/reset", methods=["POST"])
@swag_from("swagger_docs/post_reset.yaml")
def reset():
    db.drop_all()
    init_db()
    return jsonify({"message": "Banco de dados resetado"}), 200


@bp.route("/plano/<nome>", methods=["POST"])
@swag_from("swagger_docs/post_plano.yaml")
def inicia_plano(nome):
    # Verifica se o plano é válido pelo Enum PlanoNome
    try:
        plano_nome = PlanoNome(nome)
    except ValueError:
        return jsonify({"error": "Plano inválido"}), 400

    sis = Sistema.query.first()
    if sis.status == "executando":
        return jsonify({"error": "Execução em andamento"}), 400

    sis.status = "executando"
    db.session.add(sis)

    pl = Plano(nome=plano_nome.value, status="executando")
    db.session.add(pl)
    db.session.commit()
    plano_id = pl.id
    thread = threading.Thread(
        target=seleciona_plano,
        args=(
            current_app.app_context(),
            plano_id,
        ),
    )
    thread.start()

    return (
        jsonify(
            {
                "id": pl.id,
                "nome": pl.nome,
                "status": pl.status,
                "timestamp": pl.timestamp,
            }
        ),
        200,
    )
