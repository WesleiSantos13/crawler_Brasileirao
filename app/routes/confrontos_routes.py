from flask import Blueprint, jsonify
from app.services.confrontos_service import listar_confrontos

confrontos_bp = Blueprint("confrontos", __name__)

@confrontos_bp.route("/confrontos", methods=["GET"])
def get_confrontos():
    return jsonify(listar_confrontos())