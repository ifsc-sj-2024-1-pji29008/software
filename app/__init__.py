from flask import Flask
from loguru import logger
from .database import db, init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    logger.add("logs/app.log", rotation="50 MB")

    from . import routes

    app.register_blueprint(routes.bp)

    with app.app_context():
        init_db()

    return app
