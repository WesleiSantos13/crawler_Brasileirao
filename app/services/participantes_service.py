from app.database.connection import SessionLocal
from app.database.models import Participante

def listar_participantes():
    db = SessionLocal()

    dados = db.query(Participante).all()

    resultado = []
    for p in dados:
        resultado.append({
            "time": p.time.nome if p.time else None,
            "cidade": p.cidade,
            "estado": p.estado,
            "posicao_anterior": p.posicao_anterior,
            "estadio": p.estadio,
            "capacidade": p.capacidade,
            "titulos": p.titulos,
            "ano": p.ano
        })

    db.close()
    return resultado