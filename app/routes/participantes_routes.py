from flask import Blueprint, jsonify
from app.services.participantes_service import listar_participantes

participantes_bp = Blueprint("participantes", __name__)

@participantes_bp.route("/participantes", methods=["GET"])
def get_participantes():
    return jsonify(listar_participantes())