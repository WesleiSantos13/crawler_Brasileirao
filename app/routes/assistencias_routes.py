from flask import Blueprint, jsonify, request
from app.services.assistencias_service import listar_assistencias
from operator import itemgetter

assistencias_bp = Blueprint("assistencias", __name__)

# LISTAR TUDO
@assistencias_bp.route("/assistencias", methods=["GET"])
def get_assistencias():
    return jsonify(listar_assistencias())


# FILTRAR POR ANO
@assistencias_bp.route("/assistencias/ano/<int:ano>", methods=["GET"])
def assistencias_por_ano(ano):
    dados = listar_assistencias()

    filtrado = []
    for a in dados:
        if a["ano"] == ano:
            filtrado.append(a)

    return jsonify(filtrado)


#  TOP ASSISTÊNCIAS
@assistencias_bp.route("/assistencias/top", methods=["GET"])
def top_assistencias():
    top = request.args.get("top", 5, type=int)

    dados = listar_assistencias()

    # ordena pelo número de assistências
    dados.sort(key=itemgetter("assistencias"), reverse=True)

    return jsonify(dados[:top])