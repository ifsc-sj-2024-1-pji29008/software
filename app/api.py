from flask import Blueprint, jsonify, request
from loguru import logger


bp = Blueprint("api", __name__, url_prefix="/api")

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
    
    
@bp.route('/resultados', methods=['POST'])
def post_barramento_1():
    try:
        # Recebe os dados do corpo da requisição
        dados = request.json
        # Aqui você pode adicionar a lógica para processar os dados recebidos e salvar no banco de dados
        # Por exemplo, salvar os dados em uma tabela de resultados

        # Retorna uma resposta de sucesso
        return jsonify({"mensagem": "Dados recebidos com sucesso!"}), 201
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro
        return jsonify({"error": str(e)}), 500   

