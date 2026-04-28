from flask import Blueprint, jsonify
from app.services.artilharia_service import listar_artilharia

artilharia_bp = Blueprint("artilharia", __name__)

@artilharia_bp.route("/artilharia", methods=["GET"])
def get_artilharia():
    return jsonify(listar_artilharia())