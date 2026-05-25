from flask import Blueprint, jsonify, request
from app.services.artilharia_service import listar_artilharia
from operator import itemgetter

artilharia_bp = Blueprint("artilharia", __name__)

# =========================
# 1. LISTAR TUDO
# =========================
@artilharia_bp.route("/artilharia", methods=["GET"])
def get_artilharia():
    return jsonify(listar_artilharia())


# =========================
# 2. TOP ARTILHEIROS
# =========================
# https://crawlerbrasileirao-production.up.railway.app/artilharia/top
@artilharia_bp.route("/artilharia/top", methods=["GET"])
def top_artilharia():
    top = request.args.get("top", 5, type=int)

    dados = listar_artilharia()
    dados.sort(key=itemgetter("gols"), reverse=True)

    return jsonify(dados[:top])

# =========================
# 3. FILTRAR POR ANO
# =========================
#https://crawlerbrasileirao-production.up.railway.app/artilharia/2023
@artilharia_bp.route("/artilharia/ano/<int:ano>", methods=["GET"])
def artilharia_por_ano(ano):
    dados = listar_artilharia()

    filtrado = []
    for a in dados:
        if a["ano"] == ano:
            filtrado.append(a)

    return jsonify(filtrado)