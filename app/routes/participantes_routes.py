from flask import Blueprint, jsonify
from app.services.participantes_service import listar_participantes

participantes_bp = Blueprint("participantes", __name__)

@participantes_bp.route("/participantes", methods=["GET"])
def get_participantes():
    return jsonify(listar_participantes())


# LISTAR POR ANO
@participantes_bp.route("/participantes/ano/<int:ano>", methods=["GET"])
def participantes_por_ano(ano):
    dados = listar_participantes()

    resultado = []
    for p in dados:
        if p["ano"] == ano:
            resultado.append(p)

    return jsonify(resultado)


#Buscar participações por nome do time
#https://crawlerbrasileirao-production.up.railway.app/participantes/time/flamengo
@participantes_bp.route("/participantes/time/<nome>", methods=["GET"])
def participante_por_time(nome):
    dados = listar_participantes()

    resultado = []
    for p in dados:
        if nome.lower() in p["time"].lower():
            resultado.append(p)

    return jsonify(resultado)