# Define your Flask routes here

from flask import Blueprint, render_template
from loguru import logger

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    logger.info("Home page accessed")
    return render_template("index.html")
