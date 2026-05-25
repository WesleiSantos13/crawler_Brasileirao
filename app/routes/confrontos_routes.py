from flask import Blueprint, jsonify, request
from app.services.confrontos_service import listar_confrontos
from operator import itemgetter

from app.database.connection import SessionLocal
from app.database.models import Time

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
    db = SessionLocal()

    # cache pra evitar várias consultas repetidas
    cache_times = {}

    def get_nome_time(time_id):
        if time_id not in cache_times:
            time = db.query(Time).filter_by(id=time_id).first()
            cache_times[time_id] = time.nome if time else None
        return cache_times[time_id]

    # adiciona nomes e total de gols
    for c in dados:
        c["mandante"] = get_nome_time(c["mandante_id"])
        c["visitante"] = get_nome_time(c["visitante_id"])
        c["total_gols"] = c["gols_mandante"] + c["gols_visitante"]

    db.close()

    # ordena
    dados.sort(key=itemgetter("total_gols"), reverse=True)

    return jsonify(dados[:top])