from flask import Blueprint, jsonify
from app.services.hattricks_service import listar_hattricks

hattricks_bp = Blueprint("hattricks", __name__)

@hattricks_bp.route("/hattricks", methods=["GET"])
def get_hattricks():
    return jsonify(listar_hattricks())


#Filtrar por ano
@hattricks_bp.route("/hattricks/ano/<int:ano>", methods=["GET"])
def hattricks_por_ano(ano):
    dados = listar_hattricks()

    resultado = []
    for h in dados:
        if h["ano"] == ano:
            resultado.append(h)

    return jsonify(resultado)

# Buscar hat-tricks por jogador
@hattricks_bp.route("/hattricks/jogador/<nome>", methods=["GET"])
def hattricks_por_jogador(nome):
    dados = listar_hattricks()

    resultado = []
    for h in dados:
        if nome.lower() in h["jogador"].lower():
            resultado.append(h)

    return jsonify(resultado)