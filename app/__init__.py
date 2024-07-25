from flask import Flask
from loguru import logger
from .database import db, init_db


def create_app():
    # Cria a instância da aplicação Flask
    app = Flask(__name__)

    # Configura a aplicação com as configurações definidas em app/config.py
    app.config.from_object("app.config.Config")

    # Instancia o banco de dados
    db.init_app(app)

    # Configura o logger para salvar os logs em um arquivo
    logger.add("logs/app.log", rotation="50 MB")

    # Registra as rotas da interface WEB na aplicação
    from . import routes

    app.register_blueprint(routes.bp)

    # Registra as rotas da API na aplicação
    from . import api

    app.register_blueprint(api.bp)

    with app.app_context():
        # Inicializa o banco de dados
        init_db()

    return app
