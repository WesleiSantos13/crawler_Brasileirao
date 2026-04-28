from flask import Blueprint, jsonify, request
from app.services.confrontos_service import listar_confrontos
from operator import itemgetter

confrontos_bp = Blueprint("confrontos", __name__)

#  LISTAR TUDO
@confrontos_bp.route("/confrontos", methods=["GET"])
def get_confrontos():
    return jsonify(listar_confrontos())


#  FILTRAR POR ANO
@confrontos_bp.route("/confrontos/ano/<int:ano>", methods=["GET"])
def confrontos_por_ano(ano):
    dados = listar_confrontos()

    filtrado = []
    for c in dados:
        if c["ano"] == ano:
            filtrado.append(c)

    return jsonify(filtrado)




# JOGOS COM MAIS GOLS
@confrontos_bp.route("/confrontos/top-gols", methods=["GET"])
def confrontos_mais_gols():
    top = request.args.get("top", 5, type=int)

    dados = listar_confrontos()

    # cria campo total de gols
    for c in dados:
        c["total_gols"] = c["gols_mandante"] + c["gols_visitante"]

    # ordena pelos jogos com mais gols
    dados.sort(key=itemgetter("total_gols"), reverse=True)

    return jsonify(dados[:top])