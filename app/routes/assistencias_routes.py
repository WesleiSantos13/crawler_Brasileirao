from flask import Blueprint, jsonify
from app.services.assistencias_service import listar_assistencias

assistencias_bp = Blueprint("assistencias", __name__)

@assistencias_bp.route("/assistencias", methods=["GET"])
def get_assistencias():
    return jsonify(listar_assistencias())