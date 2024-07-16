# Define your Flask routes here

from flask import Blueprint, jsonify
from loguru import logger

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    logger.info('Home page accessed')
    return jsonify({"message": "Hello, World!"})
