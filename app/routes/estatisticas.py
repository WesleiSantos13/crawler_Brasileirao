from flask import Blueprint, jsonify
from app.services.confrontos_service import listar_confrontos

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats/time/<nome>", methods=["GET"])
def estatisticas_time(nome):
    dados = listar_confrontos()

    jogos = [c for c in dados if c["mandante"] == nome or c["visitante"] == nome]

    vitorias = empates = derrotas = 0

    for j in jogos:
        gm = j["gols_mandante"]
        gv = j["gols_visitante"]

        if j["mandante"] == nome:
            if gm > gv:
                vitorias += 1
            elif gm == gv:
                empates += 1
            else:
                derrotas += 1
        else:
            if gv > gm:
                vitorias += 1
            elif gm == gv:
                empates += 1
            else:
                derrotas += 1

    return jsonify({
        "time": nome,
        "jogos": len(jogos),
        "vitorias": vitorias,
        "empates": empates,
        "derrotas": derrotas
    })