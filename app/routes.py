# Define your Flask routes here

from flask import Blueprint, jsonify
from loguru import logger

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    logger.info("Home page accessed")
    return jsonify({"message": "Hello, World!"})

@bp.route('/resultados', methods=['GET'])
def get_barramento_1():
    try:
        # pega o resultados do banco de dados
        resultados = {
            "sensor1": {
                "plano_1": "PASSOU",
                "plano_2": "PASSOU",
                "plano_3": "PASSOU"
            },
            "sensor2": {
                "plano_1": "PASSOU",
                "plano_2": "PASSOU",
                "plano_3": "TEMPERATURA_ALTA"
            }
        }
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
