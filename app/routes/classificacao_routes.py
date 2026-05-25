from flask import Blueprint, jsonify, request
from operator import itemgetter
from app.services.classificacao_service import listar_classificacao

classificacao_bp = Blueprint("classificacao", __name__)

#  LISTAR TODOS
@classificacao_bp.route("/classificacao", methods=["GET"])
def get_classificacao():
    return jsonify(listar_classificacao())


#  FILTRAR POR ANO
@classificacao_bp.route("/classificacao/ano/<int:ano>", methods=["GET"])
def classificacao_por_ano(ano):
    dados = listar_classificacao()

    filtrado = []
    for c in dados:
        if c["ano"] == ano:
            filtrado.append(c)

    return jsonify(filtrado)


#  TOP POR PONTOS
@classificacao_bp.route("/classificacao/top", methods=["GET"])
def top_classificacao():
    top = request.args.get("top", 5, type=int)

    dados = listar_classificacao()

    # ordena por pontos
    dados.sort(key=itemgetter("pontos"), reverse=True)

    return jsonify(dados[:top])