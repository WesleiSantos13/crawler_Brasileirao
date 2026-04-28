from flask import Blueprint, jsonify
from app.services.classificacao_service import listar_classificacao

classificacao_bp = Blueprint("classificacao", __name__)

@classificacao_bp.route("/classificacao", methods=["GET"])
def get_classificacao():
    return jsonify(listar_classificacao())