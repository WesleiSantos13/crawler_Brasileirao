from flask import Blueprint, jsonify
from app.services.hattricks_service import listar_hattricks

hattricks_bp = Blueprint("hattricks", __name__)

@hattricks_bp.route("/hattricks", methods=["GET"])
def get_hattricks():
    return jsonify(listar_hattricks())